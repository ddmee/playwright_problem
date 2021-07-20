import sys
import os

tests_dir = os.path.dirname(os.path.abspath(__file__))
top_level = os.path.dirname(tests_dir)

sys.path.append(tests_dir)
sys.path.append(top_level)