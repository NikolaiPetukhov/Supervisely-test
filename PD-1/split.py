import argparse
import sys
import image_slicer


def validate_parameter(parameter: dict):
    s = parameter
    try:
        if s[-1] == '%':
            s = s[:-1]
            if int(s) > 100:
                return False
        if int(s) <= 0:
            return False
    except:
        return False
    return True

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-wh', '--height', default='100%', help='Height of window. Example: 50%% for percents or 1024 for pixels')
    parser.add_argument('-ww', '--width', default='100%', help='Width of window. Example: 50%% for percents or 1024 for pixels')
    parser.add_argument('-ox', '--offset-x', default='100%', help='Offset by X axis of window to slice. Example: Example: 10%% for percents or 256 for pixels')
    parser.add_argument('-oy', '--offset-y', default='100%', help='Offset by Y axis of window to slice. Example: Example: 10%% for percents or 256 for pixels')
    parser.add_argument('-sd', '--save-dir', required=False )
    parser.add_argument('image_path', nargs=1)
    args = parser.parse_args()
    height = args.height
    width = args.width
    offset_x = args.offset_x
    offset_y = args.offset_y
    image_path = args.image_path[0]
    save_dir = args.save_dir

    validate_result = (validate_parameter(height), validate_parameter(width), validate_parameter(offset_x), validate_parameter(offset_y))
    if False in validate_result:
        print('Bad arguments:\n')
        for i, param in enumerate(('Width', 'Height', 'Offset-x', 'Offset-y')):
            if not validate_result[i]:
                print(f'{param} is invalid')
        sys.exit()
    
    print((
        f'Image Path: {image_path}\n'
        f'Height: {height}\n'
        f'Width: {width}\n'
        f'Offset-x: {offset_x}\n'
        f'Offset-y: {offset_y}\n'
        f'{("Save to: "+save_dir) if save_dir else ""}'
        '\n'
    ))
    confirm = ''
    while confirm not in ('y', 'yes', 'n', 'no'):
        confirm = input('type in "Y"/"YES" to confirm. "N"/"NO" to abort.\n').lower()
    if confirm in ('n', 'no'):
        sys.exit('Aborted.')
    else:
        print('Splitting...')
        try:
            image_slicer.split(image_path, height, width, offset_x, offset_y, save_dir)
            print('Done!')
        except FileNotFoundError:
            sys.exit('File not found')
        except ValueError:
            sys.exit('Bad argument')
        except Exception as e:
            sys.exit(e)

if __name__=='__main__':
    run()
