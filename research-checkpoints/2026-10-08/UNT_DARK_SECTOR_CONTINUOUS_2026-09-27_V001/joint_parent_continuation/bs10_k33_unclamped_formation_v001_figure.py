#!/usr/bin/env python3
"""Presentation-only four-panel plot of authenticated sealed K3,3 main rows."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from reportlab.graphics.shapes import Drawing,String,Line,Rect
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF
from reportlab.lib import colors

HERE=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
DATA=HERE/'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.json'
PDF=HERE/'BS10_K33_UNCLAMPED_FORMATION_V001_FIGURE.pdf'
PROVENANCE=HERE/'BS10_K33_UNCLAMPED_FORMATION_V001_FIGURE_PROVENANCE.json'
EXPECTED='21bf1c0abaf548364665aee7d5e4559f3a0457899fcb25f3f7e35cc52d7c317b'
TIMES=[0.,1.,2.,5.,10.,20.,50.]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if PDF.exists() or PROVENANCE.exists():raise FileExistsError('Presentation outputs already exist; never overwrite')
if sha(DATA)!=EXPECTED:raise RuntimeError('Sealed K3 receipt SHA mismatch')
r=json.loads(DATA.read_text())
if r['status']!='QUALIFIED_ARITHMETIC' or r['failed_count'] or r['passed_count']!=1194:raise RuntimeError('Sealed receipt unqualified')
for path,digest in r['input_sha256'].items():
    if sha(Path(path))!=digest:raise RuntimeError('Sealed input changed: '+path)
series=[];references=[]
blue=colors.HexColor('#2467a5');orange=colors.HexColor('#ca5c26');ink=colors.HexColor('#1a2533')
styles=[(0,0.,blue,'Circle',[4,2],4.5),(0,.1,blue,'Square',None,4.5),
        (413,0.,orange,'Diamond',[1.5,2],7.),(413,.1,orange,'Triangle',None,5.5)]
for start,g,color,marker,dash,size in styles:
    h=next(item for item in r['Hamiltonians'] if item['g']==g)
    rows=[row for row in h['states'] if row['start']==start and not row['auxiliary_early_arm']]
    rows.sort(key=lambda row:row['tau'])
    if [row['tau'] for row in rows]!=TIMES:raise RuntimeError('Seven frozen main times not exact')
    for row in rows:
        if row['failed_count'] or sha(Path(row['bundle_path']))!=row['bundle_sha256']:raise RuntimeError('Row/bundle custody mismatch')
        references.append(dict(start=start,g=g,tau=row['tau'],bundle_path=row['bundle_path'],bundle_sha256=row['bundle_sha256'],bundle_index=row['bundle_index']))
    label=('Blank graph, E=25' if start==0 else 'Prepared cycle, E=1.5')+(', g=0' if g==0 else ', g=0.1')
    series.append(dict(rows=rows,label=label,color=color,marker=marker,dash=dash,size=size))

W,H=780,558;d=Drawing(W,H);d.add(Rect(0,0,W,H,fillColor=colors.white,strokeColor=None))
d.add(String(38,532,'Native record formation on a fully dynamic K3,3 slab',fontName='Helvetica-Bold',fontSize=16,fillColor=ink))
d.add(String(38,513,'All nine links and six record registers evolve; one carrier, fixed native coefficients.',fontName='Helvetica',fontSize=10,fillColor=ink))
for i,s in enumerate(series):
    x=40+(i%2)*360;y=490-(i//2)*18
    d.add(Line(x,y,x+28,y,strokeColor=s['color'],strokeWidth=1.5,strokeDashArray=s['dash']))
    mark=makeMarker(s['marker']);mark.x=x+14;mark.y=y;mark.size=s['size'];mark.strokeColor=s['color'];mark.strokeWidth=1.1
    mark.fillColor=colors.white if s['dash'] else s['color'];d.add(mark)
    d.add(String(x+36,y-3.2,s['label'],fontName='Helvetica',fontSize=10,fillColor=ink))

panels=[('A  Total occupied records','record_total',0,2.5,[0,.5,1.,1.5,2.,2.5]),
        ('B  Mean occupied links',('graph','edge_mean'),0,6.3,[0,1,2,3,4,5,6]),
        ('C  Whole-six connected probability',('graph','connected_probability'),0,1.04,[0,.25,.5,.75,1]),
        ('D  Special content visibility','fringe_visibility',0,1.04,[0,.25,.5,.75,1])]
saved_values=[]
for ip,(title,key,ymin,ymax,steps) in enumerate(panels):
    left=52+(ip%2)*370;bottom=267 if ip<2 else 78;pw,ph=322,150
    d.add(String(left,bottom+ph+15,title,fontName='Helvetica-Bold',fontSize=11.5,fillColor=ink))
    lp=LinePlot();lp.x=left;lp.y=bottom;lp.width=pw;lp.height=ph;lp.joinedLines=1
    values=[]
    for s in series:
        pairs=[(row['tau'],row[key] if isinstance(key,str) else row[key[0]][key[1]]) for row in s['rows']]
        values.append(pairs);saved_values.append(dict(panel=title,series=s['label'],pairs=pairs))
    lp.data=values
    lp.xValueAxis.valueMin=0;lp.xValueAxis.valueMax=50;lp.xValueAxis.valueSteps=[0,10,20,30,40,50]
    lp.yValueAxis.valueMin=ymin;lp.yValueAxis.valueMax=ymax;lp.yValueAxis.valueSteps=steps
    for axis in (lp.xValueAxis,lp.yValueAxis):
        axis.strokeColor=colors.HexColor('#8c98a4');axis.strokeWidth=.5;axis.labels.fontName='Helvetica';axis.labels.fontSize=8.5
        axis.labels.fillColor=ink;axis.tickStrokeColor=colors.HexColor('#8c98a4');axis.visibleGrid=1
        axis.gridStrokeColor=colors.HexColor('#e5e9ed');axis.gridStrokeWidth=.4;axis.gridStrokeDashArray=[1,2]
    lp.xValueAxis.labels.boxAnchor='n';lp.yValueAxis.labels.boxAnchor='e';lp.yValueAxis.labels.dx=-5
    for i,s in enumerate(series):
        line=lp.lines[i];line.strokeColor=s['color'];line.strokeWidth=1.4;line.strokeDashArray=s['dash']
        mark=makeMarker(s['marker']);mark.size=s['size'];mark.strokeColor=s['color'];mark.strokeWidth=.9
        mark.fillColor=colors.white if s['dash'] else s['color'];line.symbol=mark
    d.add(lp)
    if ip==2:
        d.add(String(left+112,bottom+30,'Blank: P connected ~ 10^-9',fontName='Helvetica',fontSize=9,fillColor=blue))
    if ip>=2:d.add(String(left+pw/2,bottom-28,'Native age: t U_d / hbar',textAnchor='middle',fontName='Helvetica',fontSize=9.5,fillColor=ink))
d.add(String(38,33,'Markers: saved ages 0, 1, 2, 5, 10, 20, 50. Lines only guide the eye between saved points.',fontName='Helvetica',fontSize=9,fillColor=ink))
d.add(String(38,20,'Connectivity is an undirected graph measurement probability. Visibility uses the paired pure-content witness.',fontName='Helvetica',fontSize=9,fillColor=ink))
d.add(String(38,7,'Time unit hbar/U_d is conditional; no physical time, spatial geometry or gravitational calibration is assigned.',fontName='Helvetica',fontSize=9,fillColor=ink))
pdf=renderPDF.drawToString(d)
with PDF.open('xb') as out:out.write(pdf)
proof=dict(created_utc=datetime.now(timezone.utc).isoformat(),mode='authenticated saved-data presentation only',
    sealed_result_path=str(DATA),sealed_result_sha256=EXPECTED,source_path=str(Path(__file__).resolve()),source_sha256=sha(Path(__file__)),
    pdf_path=str(PDF),pdf_sha256=sha(PDF),receipt_controls='1194/1194, four selected histories, seven frozen main points each',
    selected_bundle_references=references,plotted_values=saved_values,plotting_library='bundled ReportLab LinePlot/vector PDF',
    no_scientific_recalculation=True,joins='guides between saved points only; no inferred continuous trajectory',
    graph_scope='underlying undirected six-node incidence measurement probabilities',
    time_scope='native age t U_d/hbar; unit hbar/U_d has no physical calibration',
    content_scope='special same pure spatial/incidence seed, paired orthogonal-content branches',
    figures_scope='finite prepared histories; no geometry, gravity, irreversible sealing or superiority claim')
with PROVENANCE.open('x') as out:json.dump(proof,out,indent=2,sort_keys=True);out.write('\n')
print(json.dumps(dict(pdf_path=str(PDF),pdf_sha256=sha(PDF),provenance_path=str(PROVENANCE),source_sha256=sha(Path(__file__))),indent=2))
