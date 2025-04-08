import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from server.utils.processing_util import _process_image_pipeline

if __name__ == "__main__":
    try:
        input_path = Path(sys.argv[1])
        output_path = Path(sys.argv[2])
        _process_image_pipeline(input_path, output_path)
    except Exception as e:
        print(f"[WORKER ERROR] {e}", file=sys.stderr)
        sys.exit(1)
