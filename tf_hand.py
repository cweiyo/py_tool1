import tensorflow as tf
import numpy as np
import cv2

img_path = "/home/liusiwei/Pictures/101410/02.jpeg"
PATH_TO_CKPT = "/home/liusiwei/py_tools/output_inference_graph/frozen_inference_graph.pb"
PATH_TO_LABELS = "/home/liusiwei/py_tools/hand_label_map.pbtxt"
NUM_CLASSES = 3


class HandDetect(object):
    def __init__(self):
        # graph
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # -----------------------------------------------------------------------------------------------------------
        with detection_graph.as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
            self.sess = tf.Session(graph=detection_graph, config=tf.ConfigProto(gpu_options=gpu_options))
            self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    def detecting_ThumbsUp(self, image_path):
        """
        It processes the frame of the camera and returns the result of the detection;
        the possible results are: 'GOOD', 'OTHER', 'OK'
        """

        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        image_np_expanded = np.expand_dims(img, axis=0)

        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        # img, result = vis_util_hobin.visualize_boxes_and_labels_on_image_array(
        #     image,
        #     np.squeeze(boxes),
        #     np.squeeze(classes).astype(np.int32),
        #     np.squeeze(scores),
        #     self.category_index,
        #     use_normalized_coordinates=True,
        #     line_thickness=3)
        return (boxes, scores, classes, num)


if __name__ == "__main__":
    detect_hand = HandDetect()
    boxes, scores, classes, num = detect_hand.detecting_ThumbsUp(img_path)
    print(boxes.shape, scores.shape, classes.shape, num.shape)

    print(np.argmax(scores))
    print(classes[0, np.argmax(scores)], scores[0, np.argmax(scores)])