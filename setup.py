import argparse
import observer

parser = argparse.ArgumentParser(description='File manipulator support')
parser.add_argument('--rm', default=None, 
							required=False, 
							metavar='', 
							action='store', nargs='*',
							help='Remove the files mode')
args = parser.parse_args()

obs = observer.Observer()

if args.rm is None:
	obs.run("default_mode")
else:
	obs.run("remove_mode")
