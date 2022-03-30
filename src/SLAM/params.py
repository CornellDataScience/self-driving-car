class Params(object):
    def __init__(self):
        
        self.pnp_min_measurements = 10
        self.pnp_max_iterations = 10
        self.init_min_points = 10

        self.local_window_size = 10
        self.ba_max_iterations = 10

        self.min_tracked_points_ratio = 0.5

        self.lc_min_inbetween_frames = 10   # frames
        self.lc_max_inbetween_distance = 3  # meters
        self.lc_embedding_distance = 22.0
        self.lc_inliers_threshold = 15
        self.lc_inliers_ratio = 0.5
        self.lc_distance_threshold = 2      # meters
        self.lc_max_iterations = 20

        self.ground = False

        self.view_camera_size = 1

        self.matching_cell_size = 15   # pixels
        self.matching_neighborhood = 2
        self.matching_distance = 25

        self.frustum_near = 0.1  # meters
        self.frustum_far = 50.0

        self.lc_max_inbetween_distance = 4   # meters
        self.lc_distance_threshold = 1.5
        self.lc_embedding_distance = 22.0

        self.view_image_width = 400
        self.view_image_height = 250
        self.view_camera_width = 0.1
        self.view_viewpoint_x = 0
        self.view_viewpoint_y = -1
        self.view_viewpoint_z = -10
        self.view_viewpoint_f = 2000
