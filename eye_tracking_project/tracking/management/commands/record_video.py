# tracking/management/commands/record_video.py

from django.core.management.base import BaseCommand

from tracking.scripts.record_video import record_video


class Command(BaseCommand):
    help = 'Record video from webcam'

    def add_arguments(self, parser):
        parser.add_argument('duration', type=int, help='Duration to record video in seconds')

    def handle(self, *args, **kwargs):
        duration = kwargs['duration']
        record_video(duration=duration)
        self.stdout.write(self.style.SUCCESS("Video recorded successfully."))
