import cv2
import numpy as np
from fastiecm import fastiecm

class FastieColorMap(object):
 def apply_color_map(self, ndvi_frame):
    normalized_ndvi = (ndvi_frame + 1) / 2
    color_mapped_prep = (normalized_ndvi * 255).astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    return color_mapped_image
 
class SimulatedNDVI(object):
 def convert(self, frame):
    blue = frame[:, :, 0].astype('float')
    red = frame[:, :, 2].astype('float')
    bottom = (blue + red)
    bottom[bottom == 0] = 1 # avoid division by zero
    sim_ndvi = (red - blue) / bottom
    return sim_ndvi

def main():
    simulated_ndvi = SimulatedNDVI()
    fastie_color_map = FastieColorMap()
    cap = cv2.VideoCapture(0) 
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame")
            break
        resized_frame = cv2.resize(frame, (720, 600))
        sim_ndvi_frame = simulated_ndvi.convert(resized_frame)
    
        color_mapped_image = fastie_color_map.apply_color_map(sim_ndvi_frame)
        cv2.imshow('Fastie Color Map', color_mapped_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
 main()