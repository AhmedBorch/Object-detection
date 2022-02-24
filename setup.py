diff --git a/mediapipe/graphs/pose_tracking/upper_body_pose_tracking_gpu.pbtxt b/mediapipe/graphs/pose_tracking/upper_body_pose_tracking_gpu.pbtxt
index 5f60846..3dcc0f7 100644
--- a/mediapipe/graphs/pose_tracking/upper_body_pose_tracking_gpu.pbtxt
+++ b/mediapipe/graphs/pose_tracking/upper_body_pose_tracking_gpu.pbtxt
@@ -1,13 +1,17 @@
 # MediaPipe graph that performs upper-body pose tracking with TensorFlow Lite on GPU.
 
-# GPU buffer. (GpuBuffer)
 input_stream: "input_video"
 
-# Output image with rendered results. (GpuBuffer)
 output_stream: "output_video"
 # Pose landmarks. (NormalizedLandmarkList)
 output_stream: "pose_landmarks"
 
+node: {
+  calculator: "ImageFrameToGpuBufferCalculator"
+  input_stream: "input_video"
+  output_stream: "input_video_gpu"
+}
+
 # Throttles the images flowing downstream for flow control. It passes through
 # the very first incoming image unaltered, and waits for downstream nodes
 # (calculators and subgraphs) in the graph to finish their tasks before it
@@ -20,8 +24,8 @@ output_stream: "pose_landmarks"
 # subsequent nodes are still busy processing previous inputs.
 node {
   calculator: "FlowLimiterCalculator"
-  input_stream: "input_video"
-  input_stream: "FINISHED:output_video"
+  input_stream: "input_video_gpu"
+  input_stream: "FINISHED:output_video_gpu"
   input_stream_info: {
     tag_index: "FINISHED"
     back_edge: true
@@ -68,5 +72,11 @@ node {
   input_stream: "LANDMARKS:pose_landmarks_smoothed"
   input_stream: "ROI:roi_from_landmarks"
   input_stream: "DETECTION:pose_detection"
-  output_stream: "IMAGE:output_video"
+  output_stream: "IMAGE:output_video_gpu"
+}
+
+node: {
+  calculator: "GpuBufferToImageFrameCalculator"
+  input_stream: "output_video_gpu"
+  output_stream: "output_video"
 }
diff --git a/mediapipe/python/BUILD b/mediapipe/python/BUILD
index a48e791..0d90a31 100644
--- a/mediapipe/python/BUILD
+++ b/mediapipe/python/BUILD
@@ -20,7 +20,9 @@ cc_library(
     name = "builtin_calculators",
     deps = [
         "//mediapipe/calculators/core:pass_through_calculator",
-        "//mediapipe/graphs/pose_tracking:upper_body_pose_tracking_cpu_deps",
+        "//mediapipe/graphs/pose_tracking:upper_body_pose_tracking_gpu_deps",
+        "//mediapipe/gpu:gpu_buffer_to_image_frame_calculator",
+        "//mediapipe/gpu:image_frame_to_gpu_buffer_calculator",
     ],
 )
