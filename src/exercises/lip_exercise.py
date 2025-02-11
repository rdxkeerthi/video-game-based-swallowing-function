from utils.mediapipe_tracker import MediaPipeTracker
from utils.feedback import Feedback
import pygame
import cv2
from .base_exercise import BaseExercise

class LipExercise(BaseExercise):
    def __init__(self):
        super().__init__("Lip Exercise")
        self.rabbit_pos = [400, 300]
        self.rabbit_speed = 5
        self.rabbit_image = pygame.image.load('assets/images/rabbit.png')
        self.background = self.load_background('assets/images/background.png')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            success, frame = self.cap.read()
            if not success:
                continue

            results = self.tracker.process_frame(frame)
            left_cheek = self.tracker.get_landmark(results, 234)
            right_cheek = self.tracker.get_landmark(results, 454)

            if left_cheek and right_cheek:
                if left_cheek.y < right_cheek.y:
                    self.rabbit_pos[0] -= self.rabbit_speed
                elif right_cheek.y < left_cheek.y:
                    self.rabbit_pos[0] += self.rabbit_speed

            self.rabbit_pos[0] = max(0, min(self.rabbit_pos[0], self.screen_width - self.rabbit_image.get_width()))

            self.screen.blit(self.background, (0, 0))
            pygame.draw.rect(self.screen, (255, 0, 0), self.screen.get_rect(), 5)
            self.screen.blit(self.rabbit_image, self.rabbit_pos)
            pygame.draw.circle(self.screen, (0, 255, 0), (int(self.rabbit_pos[0] + self.rabbit_image.get_width() / 2), int(self.rabbit_pos[1] + self.rabbit_image.get_height() / 2)), 5)
            self.feedback.display_message(self.screen, "Use your cheeks to move left or right!", (10, 10))
            pygame.display.flip()

            self.clock.tick(30)
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.quit()
