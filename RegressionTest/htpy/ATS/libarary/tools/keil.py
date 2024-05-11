import os
import xmltodict
from RegressionTest.htpy.common.common_api import *


class Keil:
    home = None
    user = 'btwu'
    device = None
    usb_type = 'FS'

    keil_exe = r'C:\Keil_v5\UV4\UV4.exe'

    user_config = {
        'home_path': {
            'btwu': r'D:\TestProjects\src'
        }
    }

    uvprojx_file = None

    def __init__(self):
        pass

    @staticmethod
    def uvprojx_to_json(uvprojx_file):
        if not os.path.exists(uvprojx_file):
            print("{} keil工程不存在".format(uvprojx_file))
        else:
            json_file = uvprojx_file.replace('.uvprojx', '.json')
            dict_keil = xmltodict.parse(open(uvprojx_file, encoding='utf-8').read())
            dump_dict_to_file(dict_keil, json_file)

    @staticmethod
    def load_config(config_file, chip_name=None):
        config_dict = load_dict_from_file(config_file)
        filtered_config_dict = {}
        if chip_name is not None:
            len_chip_name = len(chip_name)
            for proj in config_dict:
                if proj[:len_chip_name] == chip_name:
                    filtered_config_dict[proj] = config_dict[proj]
        for proj in filtered_config_dict:
            print(proj)
        return filtered_config_dict

    @staticmethod
    def load_config_by_project(config_file, project=None):
        config_dict = load_dict_from_file(config_file)
        filtered_config_dict = {}
        if project is not None:
            for proj in config_dict:
                if proj == project:
                    filtered_config_dict[proj] = config_dict[proj]
        for proj in filtered_config_dict:
            print(proj)
        return filtered_config_dict

    @staticmethod
    def load_template_project(uvprojx_file):
        proj_dict = None
        if not os.path.exists(uvprojx_file):
            print("{} keil工程不存在".format(uvprojx_file))
        else:
            proj_dict = xmltodict.parse(open(uvprojx_file, encoding='utf-8').read())
        return proj_dict

    @staticmethod
    def gen_uvprojx_by_proj_and_config_dict(proj_dict, config_dict, project=None):
        for proj in config_dict:
            if project is not None and project != proj:
                continue
            config_dict[proj]['工程输出路径'] = '{}\\Project\\Users\\{}'.format(Keil.home, Keil.user)
            if config_dict[proj]['工程输出路径'] is None:
                continue
            # 1.确定工程文件名
            uvprojx_file = os.path.join(config_dict[proj]['工程输出路径'], '{}.uvprojx'.format(proj))
            print("1. 即将生成的工程文件名为：{}".format(uvprojx_file))

            # 先将相关旧文件删除
            directory_path = config_dict[proj]['工程输出路径']
            for file in os.listdir(directory_path):
                if proj in file:
                    file_path = os.path.join(directory_path, file)
                    print(f"先删除文件{file_path}")
                    os.remove(file_path)
            # 2.1 修改target名称
            proj_dict['Project']['Targets']['Target']['TargetName'] = proj
            # 2.2 修改device名称
            if Keil.device is not None:
                proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['Device'] = Keil.device
                sfd_file = proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['SFDFile']
                if sfd_file is not None:
                    p = '.*Device:(\w+)\$CMSIS.*'
                    ret = match_pattern(p, sfd_file, 1)
                    if ret is not None:
                        device = ret[0]
                        sfd_file = sfd_file.replace(device, Keil.device)
                        proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['SFDFile'] = sfd_file
            # 3. 增加源文件的分组
            group_list = []
            include_path_list = []
            for group in config_dict[proj]['文件分组']:
                if 'Inc' in config_dict[proj]['文件分组'][group]:
                    inc_list = []
                    for inc in config_dict[proj]['文件分组'][group]['Inc']:
                        inc_path = '{}\\{}'.format('..\\..\\..', inc)
                        if group.count('USB_DEVICE') > 0:
                            inc_path = inc_path.replace('\\FS', f'\\{Keil.usb_type}')
                            inc_path = inc_path.replace('\\HS', f'\\{Keil.usb_type}')
                        inc_list.append(inc_path)
                    include_path_list.append(inc_list)
                group_info = {
                    'GroupName': group,
                    'Files': {
                        'File': []
                    }
                }
                src_list = config_dict[proj]['文件分组'][group]['Src']
                src_dir = '{}\\{}'.format('..\\..\\..', config_dict[proj]['文件分组'][group]['路径'])
                if group.count('USB_DEVICE') > 0:
                    src_dir = src_dir.replace('\\FS', f'\\{Keil.usb_type}')
                    src_dir = src_dir.replace('\\HS', f'\\{Keil.usb_type}')
                if len(src_list) > 0:
                    if len(src_list) == 1:
                        src_file_name = src_list[0]
                        src_file_type = '1'
                        if src_file_name[-2:] == '.s':
                            src_file_type = '2'
                        # 单个文件信息
                        file_info = {
                            'FileName': src_file_name,
                            'FileType': src_file_type,
                            'FilePath': os.path.join(src_dir, src_file_name)
                        }
                        group_info['Files']['File'] = file_info
                    else:
                        for src_file_name in src_list:
                            src_file_type = '1'
                            if src_file_name[-2:] == '.s':
                                src_file_type = '2'
                            # 单个文件信息
                            file_info = {
                                'FileName': src_file_name,
                                'FileType': src_file_type,
                                'FilePath': os.path.join(src_dir, src_file_name)
                            }
                            group_info['Files']['File'].append(file_info)
                group_list.append(group_info)
            proj_dict['Project']['Targets']['Target']['Group'] = group_list

            # 4. 更新include path
            include_path_str = ''
            for inc in include_path_list:
                include_path_str = '{};{}'.format(include_path_str, inc)
            if len(include_path_str) > 0:
                include_path_str = include_path_str[1:]

            proj_dict['Project']['Targets']['Target']['TargetOption']['TargetArmAds']['Cads']['VariousControls']['IncludePath'] = include_path_str

            # 5. 更新宏定义列表
            define_str = ''
            for define in config_dict['宏定义列表']:
                define_str = '{},{}'.format(define_str, define)
            # 添加USB FS/HS的宏定义
            define_str = '{},{}'.format(define_str, f'FEA_WITH_USB_{Keil.usb_type}')
            if len(define_str) > 0:
                define_str = define_str[1:]
            proj_dict['Project']['Targets']['Target']['TargetOption']['TargetArmAds']['Cads']['VariousControls']['Define'] = define_str

            # 6. 修改输出文件名称
            proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['OutputName'] = proj
            proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['OutputDirectory'] = '.\\Output\\'

            # 7. 修改输出文件路径
            output_dir = config_dict[proj].get('OutPutDirectory')
            listing_dir = config_dict[proj].get('ListingPath')
            if output_dir is not None:
                proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['OutputDirectory'] = output_dir
            if listing_dir is not None:
                proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['ListingPath'] = listing_dir

            proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['OutputDirectory'] = f'.\\Output\\{proj}\\'
            proj_dict['Project']['Targets']['Target']['TargetOption']['TargetCommonOption']['ListingPath'] = f'.\\Output\\{proj}\\'

            with open(uvprojx_file, 'wb') as f:
                xmltodict.unparse(proj_dict, f)

            Keil.uvprojx_file = uvprojx_file

    @staticmethod
    def get_user_home_path(user):
        user_home_path = Keil.user_config['home_path'].get(user)
        if user_home_path is None:
            print(f'需要在keil.Keil.user_config中配置用于{user}的代码路径信息')
        return user_home_path

    @staticmethod
    def update_project(user, project, template):
        home_path = Keil.get_user_home_path(user)
        Keil.home = home_path + r'\c\AutoTestFirmware'
        Keil.user = user

        project_path = '{}\\Project'.format(Keil.home)
        uvprojx_file = '{}\\Users\\template\{}_template.uvprojx'.format(project_path, template)
        config_file = home_path + r'\python\RegressionTest\htpy\ATS\library\tools\config.json'
        # 1. 加载配置文件
        config_dict = Keil.load_config_by_project(config_file, project)
        # 2. 加载模板
        proj_dict = Keil.load_template_project(uvprojx_file)
        # 3. 根据样例工程生成keil工程
        Keil.gen_uvprojx_by_proj_and_config_dict(proj_dict, config_dict)

    @staticmethod
    def build(uvprojx_file=None):
        if uvprojx_file is None:
            uvprojx_file = Keil.uvprojx_file
        log_file = uvprojx_file.replace('.uvprojx', '.txt')
        cmd = f'{Keil.keil_exe} -j0 -r {uvprojx_file} -0 {log_file}'
        out = os.popen(cmd)

        # 如果去掉一下处理，则可能还未编译完就去检查编译日志，会出错
        for l in out.readlines():
            print(l.decode('GB2312'))

        f = open(log_file, 'r')
        lines = f.readlines()
        f.close()

        expected_list = ['0 Error(s)']
        for expected_str in expected_list:
            if str(lines).count(expected_str) == 0:
                print('编译错误')
            else:
                print('没有错误')

    @staticmethod
    def programming():
        pass


if __name__ == '__main__':

    user = 'btwu'
    project = 'H2218_ATS_V1'
    template = 'H2218'

    device = None
    Keil.device = device

    Keil.update_project(user, project, template)
    Keil.build()
