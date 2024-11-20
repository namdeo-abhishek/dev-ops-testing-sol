import os
import shutil
import zipfile
import subprocess
import pytest
import logging

# Fixture for setup and teardown
@pytest.fixture(scope="module")
def setup_teardown(tmpdir_factory):
    cwd = os.path.join(os.environ["HOME"],os.environ["NAME"])
    result = subprocess.run(["bash","init.sh"], capture_output=True, text=True,cwd=cwd)
    assert result.returncode == 0, f"init.sh failed: {result.stderr}"

    res = {
        "cool1_content" : "cool1\n",
        "cool2_content" : "cool2\n",
        "cwd" : cwd
    }
    # Yield the paths for test cases
    yield res

    if os.path.exists("/tmp/archive.zip"):
        os.remove("/tmp/archive.zip")
    if res.get("solution.sh_stdout"):
        print("\n\nOutput of solution.sh")
        print("---------------------")
        print(res["solution.sh_stdout"])
        print(res["solution.sh_stderr"])

# Testcase 1: Check if /tmp/archive.zip is created after executing solution.sh
def test_archive_zip_created(setup_teardown):

    # Step 2: Execute the solution.sh file
    result = subprocess.run(["bash", "solution.sh"], capture_output=True, text=True,cwd=setup_teardown["cwd"])
    setup_teardown["solution.sh_stdout"] = result.stdout 
    setup_teardown["solution.sh_stderr"] = result.stdout
    setup_teardown["solution.sh_returncode"] = result.returncode
    assert result.returncode == 0, f"solution.sh failed: {result.stderr}"

    # Step 3: Verify /tmp/archive.zip is created
    archive_path = "/tmp/archive.zip"
    assert os.path.exists(archive_path), "/tmp/archive.zip was not created"

# Testcase 2: Extract /tmp/archive.zip and check that it contains only cool1.txt and cool2.txt
def test_archive_contents(setup_teardown):
    archive_path = "/tmp/archive.zip"
    assert os.path.exists(archive_path), "/tmp/archive.zip not found for extraction"

    # Extract /tmp/archive.zip
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall("/tmp/extracted")

    extracted_files = os.listdir("/tmp/extracted/tmp/final_archive")
    
    # Check for only cool1.txt and cool2.txt
    assert "cool1.txt" in extracted_files, "cool1.txt not found in archive"
    assert "cool2.txt" in extracted_files, "cool2.txt not found in archive"
    assert len(extracted_files) == 2, "Archive contains more than the expected files"

# Testcase 3: Verify that cool1.txt and cool2.txt have the same content as in stub.zip
def test_file_content_match(setup_teardown):
    # Step 1: Read contents of extracted cool1.txt and cool2.txt
    with open("/tmp/extracted/tmp/final_archive/cool1.txt", 'r') as f:
        cool1_content = f.read()
    
    with open("/tmp/extracted/tmp/final_archive/cool2.txt", 'r') as f:
        cool2_content = f.read()

    # Step 2: Verify the contents match the original files in stub
    assert cool1_content == setup_teardown["cool1_content"], "cool1.txt content mismatch"
    assert cool2_content == setup_teardown["cool2_content"], "cool2.txt content mismatch"

    # Cleanup extracted files after the test
    shutil.rmtree("/tmp/extracted")


