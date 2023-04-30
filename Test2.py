from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar
import asyncio
import git
import threading
from enum import Enum

class Execution(Enum):
    Passed = 1
    Failed = 2

async def download_git_repo_async(repo_url: str, local_path: str, callback_fn=None) -> Execution:
    try:
        # Clone the Git repository asynchronously
        await asyncio.create_task(git.Repo.clone_from(repo_url, local_path, progress=callback_fn))
        return Execution.Passed
    except Exception as e:
        print(f"Failed to download Git repo: {e}")
        return Execution.Failed

def start_download_thread(repo_url: str, local_path: str, progress_bar: MDProgressBar, callback_fn=None):
    # Define the function to run in the separate thread
    def download_thread():
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Define the progress update function for the callback
        def update_progress(op_code, cur_count, max_count=None, message=''):
            # Update the progress bar with the current progress
            progress = cur_count / max_count if max_count else 0
            progress_bar.value = progress * 100

        # Call the download_git_repo_async function asynchronously with the progress update callback
        loop.run_until_complete(download_git_repo_async(repo_url, local_path, update_progress))

        # Stop the event loop
        loop.stop()
        loop.close()

    # Start a new thread for the download function
    thread = threading.Thread(target=download_thread)
    thread.start()

class MyApp(MDApp):
    def build(self):
        # Create a progress bar to display the download progress
        self.progress_bar = MDProgressBar(value=0, max=100)
        return self.progress_bar

    def on_start(self):
        # Start the download function in a separate thread
        start_download_thread(repo_url='https://github.com/username/repo.git',
                               local_path='/path/to/local/folder',
                               progress_bar=self.progress_bar)

if __name__ == "__main__":
    MyApp().run()