"""Small rerunnable custody/restart tests; no galaxy field solve or velocities."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
import numpy as np
import fixed_source_transfer as transfer


class TransferTests(unittest.TestCase):
    def test_control_radii(self):
        values = [.372, .948, 1.812, 3.612, 7.212]
        np.testing.assert_array_equal(transfer.validate_radii(values), values)
        for bad in ([], [1, 2, 3, 4], [0, 1, 2, 3, 4], [1, 2, 2, 4, 5],
                    [2, 1, 3, 4, 5], [1, 2, 3, 4, np.nan], [1, 2, 3, 4, np.inf]):
            with self.subTest(bad=bad), self.assertRaises(AssertionError):
                transfer.validate_radii(bad)

    def test_restart_and_refusals(self):
        with tempfile.TemporaryDirectory(prefix='unt-transfer-checkpoint-') as folder:
            path = Path(folder)/'case.checkpoint.npz'
            phi = np.arange(16, dtype='float64').reshape(4, 4)
            history = [{'nonlinear_error': .01, 'flux_balance_error': .001}]
            with contextlib.redirect_stdout(io.StringIO()):
                transfer.checkpoint_writer(path, 'case', 'freeze')(phi, history)
            actual, old_history = transfer.load_checkpoint(path, 'case', 'freeze', 4)
            np.testing.assert_array_equal(actual, phi)
            self.assertEqual(old_history, history)
            for case, freeze, n in (('other', 'freeze', 4), ('case', 'other', 4),
                                   ('case', 'freeze', 5)):
                with self.subTest(case=case, freeze=freeze, n=n), self.assertRaises(AssertionError):
                    transfer.load_checkpoint(path, case, freeze, n)
            # Replace only this disposable test checkpoint, preserving real evidence.
            history.append({'nonlinear_error': .001, 'flux_balance_error': .0001})
            with contextlib.redirect_stdout(io.StringIO()):
                transfer.checkpoint_writer(path, 'case', 'freeze')(phi+1, history)
            actual, old_history = transfer.load_checkpoint(path, 'case', 'freeze', 4)
            np.testing.assert_array_equal(actual, phi+1)
            self.assertEqual(old_history, history)

    def test_atomic_publication_and_authentication(self):
        with tempfile.TemporaryDirectory(prefix='unt-transfer-publication-') as folder:
            path = Path(folder)/'case.json'
            payload = {'finite': 1.25, 'checks': {'synthetic': True}}
            transfer.publish(path, payload, 'freeze')
            self.assertEqual(transfer.authenticated(path, 'freeze'), payload)
            with self.assertRaises(AssertionError):
                transfer.authenticated(path, 'other')
            with self.assertRaises(FileExistsError):
                transfer.publish(path, {'replaced': True}, 'freeze')
            self.assertEqual(transfer.authenticated(path, 'freeze'), payload)


if __name__ == '__main__':
    unittest.main()
