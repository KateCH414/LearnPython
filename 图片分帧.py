import os
import re


class VideoProcessUtil:
    def videoToJPG(self, video_path):
        """
        :param:
            video_path：分帧的视频路径
        :return:
            同路径下生成分帧后的图片路径
        """
        video_name_list = os.listdir(video_path)
        video_name_list = [name for name in video_name_list if name.endswith(".mp4") or name.endswith(".MP4")]
        image_dir_list = []
        for video_name in video_name_list:
            jpg_dir_path = video_path + "/" + video_name[:-4]
            if not os.path.exists(jpg_dir_path):
                os.mkdir(jpg_dir_path)
            else:
                os.system("rm -rf %s " % jpg_dir_path)
                os.mkdir(jpg_dir_path)
            os.system(
                "ffmpeg -i %s -r %0.12f -f image2 %s" % (video_path + "/" + video_name, 1, jpg_dir_path) + "/%05d.png")
            image_dir_list.append(jpg_dir_path)
        return image_dir_list


class ImageProcessUtil:
    def process_image_data(self, image_path, result_path):
        image_list = os.listdir(image_path)
        for image in image_list:
            image_file_path = image_path + "/" + image
            print(image_file_path)

            os.system("tesseract " + image_file_path + " tmp")
            with open(image_path + "/data", "a+") as result_file:
                with open("tmp.txt", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if "MB" in line:
                            result_file.write(line)
                            break;
                f.close()
            result_file.close()


class PerformanceDataProcess:
    def process_data(self, file_path):
        cpu_count = 0
        gpu_count = 0
        mem_count = 0
        max_cpu = 0
        max_memory = 0
        max_gpu = 0

        with open(file_path, "r") as f:
            data_list = f.readlines()
            for data in data_list:
                try:
                    cpu = re.findall(r"\d+\.?\d*", data.split("%")[0])[0]
                    gpu = re.findall(r"\d+\.?\d*", data)[-1]
                except IndexError as e:
                    print(data)
                    continue
                if len(cpu.split("%")[0].split(".")) != 2:
                    cpu = float(cpu) / 10
                else:
                    cpu = float(cpu)
                if len(gpu.split("%")[0].split(".")) != 2:
                    gpu = float(gpu) / 10
                else:
                    gpu = float(gpu)
                try:
                    mem = re.findall(r"\d+\.?\d*", data.split("%")[1])[0]
                except IndexError as e:
                    print(data)
                    continue
                if len(mem.split(".")) != 2:
                    mem = float(mem) / 10
                else:
                    mem = float(mem)
                cpu_count += cpu
                gpu_count += gpu
                mem_count += mem
                if mem > max_memory:
                    max_memory = mem
                if cpu > max_cpu:
                    max_cpu = cpu
                if gpu > max_gpu:
                    max_gpu = gpu
            result = ""
            result += file_path + " avr cpu is " + str(cpu_count / len(data_list)) + "\n"
            result += file_path + " max cpu is " + str(max_cpu) + "\n"
            result += file_path + " avr mem is " + str(mem_count / len(data_list)) + "\n"
            result += file_path + " max mem is " + str(max_memory) + "\n"
            result += file_path + " avr gpu is " + str(gpu_count / len(data_list)) + "\n"
            result += file_path + " max gpu is " + str(max_gpu) + "\n"
            return result


if __name__ == '__main__':
    video_path = "/Users/vickys/testdir/高拍仪"
    image_dir_list = VideoProcessUtil().videoToJPG(video_path)

    result = ""
    for image_dir in image_dir_list:
        ImageProcessUtil().process_image_data(image_dir, image_dir + "/" + "data")
        result += PerformanceDataProcess().process_data(image_dir + "/" + "data")
    print(result)




