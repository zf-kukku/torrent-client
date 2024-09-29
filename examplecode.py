import libtorrent as lt
import time
import os

def load_torrent(torrent_file):
    """
    Load the .torrent file and return a libtorrent torrent_info object.
    """
    try:
        info = lt.torrent_info(torrent_file)
        return info
    except Exception as e:
        print(f"Error loading torrent file: {e}")
        return None

def start_session(torrent_info, download_path):
    """
    Start a libtorrent session and begin downloading the torrent.
    """
    ses = lt.session()
    ses.listen_on(6881, 6891)

    # Add the torrent to the session
    params = {
        'save_path': download_path,
        'ti': torrent_info
    }
    handle = ses.add_torrent(params)
    print(f"Downloading {handle.name()}...")

    return ses, handle

def download_torrent(handle):
    """
    Manage the download process and display status updates.
    """
    while not handle.is_seed():
        s = handle.status()
        print(f"Progress: {s.progress * 100:.2f}% "
              f"downloading: {s.download_rate / 1000:.2f} kB/s "
              f"uploading: {s.upload_rate / 1000:.2f} kB/s "
              f"peers: {s.num_peers}")
        
        time.sleep(1)

    print(f"Download complete: {handle.name()}")

def main(torrent_file, download_path):
    """
    Main function to load, download, and manage the torrent session.
    """
    # Load the torrent
    torrent_info = load_torrent(torrent_file)
    if not torrent_info:
        return

    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Start a session and download the torrent
    ses, handle = start_session(torrent_info, download_path)
    
    # Start downloading
    download_torrent(handle)

    # Clean up the session
    ses.pause()

if __name__ == '__main__':
    torrent_file = '/content/changename.torrent'  # Example: 'myfile.torrent'
    download_path = '/content'  # Example: '/downloads/'
    main(torrent_file, download_path)
