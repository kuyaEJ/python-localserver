from test import Path
paths = []

def testPaths():
    index = 0
    for key, path, cwd, dres in paths:
        try:
            path.setcwd(cwd)
            if dres:
                print('PASSED - PASSING', str(len(paths) - index) + f'/{len(paths)}')
            else:
                index += 1
                print('FAILED - PASSING', str(len(paths) - index) + f'/{len(paths)}')
        except ValueError:
            if not dres:
                print('PASSED - PASSING', str(len(paths) - index) + f'/{len(paths)}')
            else:
                index += 1
                print('FAILED - PASSING', str(len(paths) - index) + f'/{len(paths)}')
    print(f'Results: {len(paths) - index} out of {len(paths)} cases passed')
    if len(paths) - index == len(paths):
        print("Success, all tests passed!")

def createTests():
    # (key, pathObj, pathString, desiredResult)
    paths.append(('1', Path(), '', True))
    paths.append(('2', Path(), '/usr/var', True))
    paths.append(('3', Path(), '/User/The/Docs.git\\docs/part', False))
    paths.append(('4', Path(), '/User/The/Docs.git\\docs/part.text\\ab', False))
    paths.append(('5', Path(), '/', True))

createTests()
testPaths()