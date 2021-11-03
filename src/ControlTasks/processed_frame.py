# # break up into smaller control tasks as needed
# from .control_task_base import ControlTaskBase
# from src.vision.process_frame import process_frame

# class ProcessedFrame(ControlTaskBase):     
#     def default(self):
#         curr_frame = self.sfr.get('curr_frame')
#         self.sfr.set('processed_frame', curr_frame)

#     def execute(self):
#         prev_frame = self.sfr.get('prev_frame')
#         curr_frame = self.sfr.get('curr_frame')
#         self.sfr.set('processed_frame', process_frame(prev_frame, curr_frame))
