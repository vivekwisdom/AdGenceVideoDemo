import argparse
import sys
import time

from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)


def analyze_shots(path):
    """ Detects camera shot changes. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.SHOT_CHANGE_DETECTION, enums.Feature.LABEL_DETECTION ]
    operation = video_client.annotate_video(path, features)
    print('\nProcessing video for shot change annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(20)

    print('\nFinished processing.')

    results = operation.result().annotation_results[0]

    for note, shot in enumerate(results.shot_annotations):
        print('Scene {}: {} to {}'.format(
            note,
            shot.start_time_offset,
            shot.end_time_offset))

    for label in results.label_annotations:
        print('Label description: {}'.format(label.description))
        print('Locations:')

        for l, location in enumerate(label.locations):
            print('\t{}: {} to {}'.format(
                l,
                location.segment.start_time_offset,
                location.segment.end_time_offset))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help='GCS path for shot change detection.')
    args = parser.parse_args()

    analyze_shots(args.path)