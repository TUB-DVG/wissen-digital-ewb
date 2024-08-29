import unittest
import subprocess


class TestRunScript(unittest.TestCase):
    def test_run_script(self):
        # Test the script without any alias
        result = subprocess.run(
            ["./run", "build", "dev"], capture_output=True, text=True
        )
        # breakpoint()
        self.assertEqual(result.stderr, "", f"Got stderr: {result.stderr}")

        # Set the temporary alias and execute the command
        result = subprocess.run(
            [
                "bash",
                "-c",
                "alias docker-compose='docker compose' && ./run build dev",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stderr, "", f"Got stderr: {result.stderr}")


if __name__ == "__main__":
    unittest.main()
