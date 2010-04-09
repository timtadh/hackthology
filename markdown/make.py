import markdown
import sys

sys.stdout.write(markdown.markdown(sys.stdin.read()))
