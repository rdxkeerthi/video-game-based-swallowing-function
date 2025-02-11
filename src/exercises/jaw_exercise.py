import pygame
import cv2
from utils.mediapipe_tracker import MediaPipeTracker
from utils.feedback import Feedback

class JawExercise:
    def __init__(self):
        self.tracker = MediaPipeTracker()
        self.feedback = Feedback()
        self.bird_pos = [400, 300]
        self.gravity = 1
        self.jump_strength = -10
        self.bird_velocity = 0
        self.window_width = 800
        self.window_height = 600
        self.is_jaw_open = False

    def initialize_pygame(self):
        """Initialize pygame components."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Jaw Exercise Game")
        self.bird_image = pygame.image.load('assets/images/bird.png')
        self.background = pygame.image.load('assets/images/sky_background.png')
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))

    def initialize_webcam(self):
        """Initialize the webcam for tracking jaw movement."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            exit(1)

    def check_jaw_movement(self, frame):
        """Check jaw position to determine if it is open."""
        results = self.tracker.process_frame(frame)
        jaw = self.tracker.get_landmark(results, 152)  # Jaw landmark ID
        
        if jaw and jaw.y < 0.5:  # Jaw is considered open if its y-position is below a threshold
            if not self.is_jaw_open:
                self.is_jaw_open = True
                self.bird_velocity = self.jump_strength  # Jump the bird when jaw opens
        else:
            self.is_jaw_open = False

    def update_bird_position(self):
        """Update bird's vertical position based on gravity and velocity."""
        self.bird_velocity += self.gravity
        self.bird_pos[1] += self.bird_velocity

        if self.bird_pos[1] > self.window_height - self.bird_image.get_height():
            self.bird_pos[1] = self.window_height - self.bird_image.get_height()  # Prevent bird from going below the ground
            self.bird_velocity = 0

    def run(self):
        """Main game loop."""
        self.initialize_pygame()
        self.initialize_webcam()
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            success, frame = self.cap.read()
            if not success:
                continue

            # Check for jaw movement
            self.check_jaw_movement(frame)

            # Update bird's position
            self.update_bird_position()

            # Draw the background and bird
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.bird_image, self.bird_pos)

            # Display feedback message
            self.feedback.display_message(self.screen, "Open your jaw to make the bird jump!", (10, 10))

            # Update the screen
            pygame.display.flip()
            clock.tick(30)

            # Show the webcam feed
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Exit if 'Esc' key is pressed
                break

        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = JawExercise()
    game.run()
