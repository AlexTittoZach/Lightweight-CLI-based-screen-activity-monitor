from pathlib import Path
import os
import atexit
import psutil

LOCK_FILE = (
    Path(__file__).resolve().parent
    / "tracker.lock"
)

def acquire_lock():

    if LOCK_FILE.exists():

        try:

            pid = int(
                LOCK_FILE.read_text()
            )
            
            if psutil.pid_exists(pid):

                return False
            
            LOCK_FILE.unlink()

        except Exception as e:

            print("Exception:", e)

            LOCK_FILE.unlink()

    LOCK_FILE.write_text(
        str(os.getpid())
    )

    atexit.register(
        release_lock
    )

    return True


def release_lock():

    if LOCK_FILE.exists():

        LOCK_FILE.unlink()
        
        