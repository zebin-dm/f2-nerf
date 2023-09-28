import os
import numpy as np
from shutil import copyfile
from omegaconf import OmegaConf, DictConfig
from glob import glob
import hydra

backup_file_patterns = [
    './CMakeLists.txt',
    './*.cpp',
    './*.h',
    './*.cu',
    './src/*.cpp',
    './src/*.h',
    './src/*.cu',
    './src/*/*.cpp',
    './src/*/*.h',
    './src/*/*.cu',
    './src/*/*/*.cpp',
    './src/*/*/*.h',
    './src/*/*/*.cu',
]


def make_image_list(data_path, factor):
    image_list = []
    suffix = ['*.jpg', '*.png', '*.JPG', '*.jpeg']
    if 0.999 < factor < 1.001:
        for suf in suffix:
            image_list += glob(f"{data_path}/images/{suf}")
    else:
        f_int = int(np.round(factor))
        for suf in suffix:
            image_list += glob(
                os.path.join(data_path, 'images_{}'.format(f_int), suf))

    assert len(image_list) > 0, "No image found"
    image_list.sort()

    f = open(os.path.join(data_path, 'image_list.txt'), 'w')
    for image_path in image_list:
        f.write(image_path + '\n')


@hydra.main(version_base=None, config_path='../confs', config_name='default')
def main(conf: DictConfig) -> None:
    if 'work_dir' in conf:
        base_dir = conf['work_dir']
    else:
        base_dir = os.getcwd()

    print('Working directory is {}'.format(base_dir))
    data_path = f"{conf['data_path']}/{conf['dataset_name']}"
    base_exp_dir = os.path.join(base_dir, 'exp', conf['dataset_name'],
                                conf['exp_name'])

    os.makedirs(base_exp_dir, exist_ok=True)

    make_image_list(data_path, conf['dataset']['factor'])

    conf = OmegaConf.to_container(conf, resolve=True)
    conf['dataset']['data_path'] = data_path
    conf['base_dir'] = base_dir
    conf['base_exp_dir'] = base_exp_dir
    config_file = f'{base_exp_dir}/runtime_config.yaml'
    OmegaConf.save(conf, config_file)
    os.system('cmake --build build --target main --config RelWithDebInfo -j')

    for build_dir in ['build', 'cmake-build-release']:
        if os.path.exists('{}/{}/main'.format(base_dir, build_dir)):
            os.system(f'{base_dir}/{build_dir}/main {config_file}')
        else:
            assert False, 'Can not find executable file'


if __name__ == '__main__':
    main()
