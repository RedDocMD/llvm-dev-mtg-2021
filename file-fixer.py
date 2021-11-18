import os
import re
import shutil

if __name__ == "__main__":
    base_dir = 'slides-export'
    pngs = [f for f in os.listdir(base_dir)]

    def add_suffix(name):
        fmt = re.compile(r'^(\d+).png$')
        m = fmt.match(name)
        if m:
            return '{}-0.png'.format(m[1])
        else:
            return name

    new_pngs = list(map(add_suffix, pngs))
    for old, new in zip(pngs, new_pngs):
        if old != new:
            shutil.copyfile(f'{base_dir}/{old}', f'{base_dir}/{new}')
            os.remove(f'{base_dir}/{old}')
