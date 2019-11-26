import configparser

class OverlayConfig():
    def __init__(self, colored_noise=True, opacity=0.7):
        self.colored_noise = colored_noise
        self.opacity = opacity


class CameraConfig():
    def __init__(self, camera_id=0, capture_interval=1):
        self.id = camera_id
        self.capture_interval = capture_interval


class Config:
    def __init__(self, colored_noise=True, opacity=0.7, camera_id=0, capture_interval=1):
        self.overlay = OverlayConfig(
            colored_noise=colored_noise, 
            opacity=opacity
        )
        self.camera = CameraConfig(
            capture_interval=capture_interval,
            camera_id=camera_id
        )


def parse_config(filename=None):

    config = Config(
        colored_noise=True,
        opacity=0.7,
        camera_id=0,
        capture_interval=1
    )

    if not (filename is None):
        config_parser = configparser.ConfigParser()
        config_parser.read(filename)

        if 'OVERLAY' in config_parser.sections():
            if 'ColoredNoise' in config_parser['OVERLAY']:
                config.overlay.colored_noise = config_parser['OVERLAY']['ColoredNoise'].lower() in ['yes', 'true']
            if 'Opacity' in config_parser['OVERLAY']:
                config.overlay.opacity = float(config_parser['OVERLAY']['Opacity'])
        if 'CAMERA' in config_parser.sections():
            if 'Camera' in config_parser['CAMERA']:
                config.camera.id = int(config_parser['CAMERA']['Camera'])
            if 'CaptureInterval' in config_parser['CAMERA']:
                config.camera.capture_interval = float(config_parser['CAMERA']['CaptureInterval'])

    return config
    