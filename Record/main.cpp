//! [headers]
#include <iostream>
#include <stdio.h>
#include <cmath>
#include <iomanip>
#include <time.h>
#include <signal.h>
#include <opencv2/opencv.hpp>
#include <fstream>
#include <NiTE.h>
//! [headers]

using namespace std;
using namespace cv;

bool protonect_shutdown = false; // Whether the running application should shut down.
bool recording = false;
int recordIndex = 0;

void DrawPoint(Mat image, int x, int y, int size, Vec3b color)
{
    for (int i = x - size/2; i <= x + size/2; ++i)
    {
        for (int j = y - size/2; j < y + size/2; ++j)
        {
            if (i >= 0 && j >= 0 && i < image.rows && j < image.cols)
            {
                // cout << "Painting at" << i << " " << j << endl;
                image.at<Vec3b>(i, j) = color;
            }
        }
    }
}

void DrawLimb(nite::UserTracker* userTracker, const nite::SkeletonJoint& joint1, const nite::SkeletonJoint& joint2, Mat frame)
{
    float coordinates[6] = {0};
    userTracker->convertJointCoordinatesToDepth(joint1.getPosition().x, joint1.getPosition().y, joint1.getPosition().z, &coordinates[0], &coordinates[1]);
    userTracker->convertJointCoordinatesToDepth(joint2.getPosition().x, joint2.getPosition().y, joint2.getPosition().z, &coordinates[3], &coordinates[4]);

    // coordinates[0] *= 3;
    // coordinates[1] *= 3;
    // coordinates[3] *= 3;
    // coordinates[4] *= 3;

    // cout << joint1.getType() << " X: " << coordinates[0] << " Y: " << coordinates[1] << endl;
    // frame.at<Vec3b>(std::round(coordinates[0]), std::round(coordinates[1])) = Vec3b(255, 0, 0);
    DrawPoint(frame, std::round(abs(coordinates[1])), std::round(abs(coordinates[0])), 20, Vec3b(255, 0, 0));
    DrawPoint(frame, std::round(abs(coordinates[4])), std::round(abs(coordinates[3])), 20, Vec3b(255, 0, 0));
    // cout << joint2.getType() << " X: " << coordinates[3] << " Y: " << coordinates[4] << endl; 
}

void DrawSkeleton(nite::UserTracker* userTracker, const nite::UserData& userData, Mat frame, ofstream& skeletonFile)
{
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_HEAD), userData.getSkeleton().getJoint(nite::JOINT_NECK), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_LEFT_ELBOW), frame);
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_ELBOW), userData.getSkeleton().getJoint(nite::JOINT_LEFT_HAND), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_ELBOW), frame);
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_ELBOW), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HAND), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_TORSO), frame);
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_SHOULDER), userData.getSkeleton().getJoint(nite::JOINT_TORSO), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_TORSO), userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), frame);
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_TORSO), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), frame);


    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_HIP), userData.getSkeleton().getJoint(nite::JOINT_LEFT_KNEE), frame);
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_LEFT_KNEE), userData.getSkeleton().getJoint(nite::JOINT_LEFT_FOOT), frame);

    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_HIP), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_KNEE), frame);
    DrawLimb(userTracker, userData.getSkeleton().getJoint(nite::JOINT_RIGHT_KNEE), userData.getSkeleton().getJoint(nite::JOINT_RIGHT_FOOT), frame);

    if (recording) {
        for (int i = 0; i <= nite::JOINT_RIGHT_FOOT; ++i)
        {
            nite::SkeletonJoint joint = userData.getSkeleton().getJoint((nite::JointType)i);
            nite::Point3f position = joint.getPosition();
            skeletonFile << position.x << " " << position.y << " " << position.z;

            if (i == nite::JOINT_RIGHT_FOOT)
            {
                skeletonFile << endl;
            }
            else
            {
                skeletonFile << ", ";
            }
        }
    }
}

void sigint_handler(int s)
{
  protonect_shutdown = true;
}

int main()
{
    std::cout << "Streaming from Kinect One sensor!" << std::endl;

    protonect_shutdown = false;

    openni::Device dev;
    openni::Status rc = openni::OpenNI::initialize();
    nite::UserTracker userTracker;
    openni::VideoStream color;

    if (rc != openni::STATUS_OK)
    {
        printf("Failed to initialize OpenNI\n%s\n", openni::OpenNI::getExtendedError());
        return rc;
    }

    const char* deviceUri = openni::ANY_DEVICE;

    rc = dev.open(deviceUri);
    if (rc != openni::STATUS_OK)
    {
        printf("Failed to open device\n%s\n", openni::OpenNI::getExtendedError());
        return rc;
    }

    nite::NiTE::initialize();

    if (userTracker.create(&dev) != nite::STATUS_OK)
    {
        return openni::STATUS_ERROR;
    }

    if (color.create(dev, openni::SENSOR_COLOR) == openni::STATUS_OK)
    {
        if (color.start() != openni::STATUS_OK)
        {
            cout << "Couldn't start color stream: " << openni::OpenNI::getExtendedError() << endl;
            color.destroy();
        }
    }
    else
    {
        cout << "Couldn't find color stream: " << openni::OpenNI::getExtendedError() << endl;
    }

    if (!color.isValid())
    {
        cout << "No valid color stream" << endl;
        return 2;
    }

    Mat rgbmat, videomat, imgToShow;
    VideoWriter videowriter;
    ofstream skeletonFile;

    //! [loop start]
    while(!protonect_shutdown)
    {
        nite::UserTrackerFrameRef userTrackerFrame;
        openni::VideoFrameRef rgb;

        if (color.readFrame(&rgb) != openni::STATUS_OK)
        {
            cout << "Read color frame failed" << endl;
            continue;
        }

        cv::Mat(rgb.getHeight(), rgb.getWidth(), CV_8UC3, (void*)rgb.getData()).copyTo(rgbmat);
        cv::Mat(rgb.getHeight(), rgb.getWidth(), CV_8UC3, (void*)rgb.getData()).copyTo(imgToShow);

        if (userTracker.readFrame(&userTrackerFrame) != nite::STATUS_OK)
        {
            cout << "Get User data failed" << endl;
            continue;
        }

        const nite::Array<nite::UserData>& users = userTrackerFrame.getUsers();

        for (int i = 0; i < users.getSize(); i++) {
            const nite::UserData& user = users[i];

            if (user.isNew())
            {
                userTracker.startSkeletonTracking(user.getId());
            }
            else if (!user.isLost())
            {
                switch(user.getSkeleton().getState())
                {
                    case nite::SKELETON_NONE:
                        cout << "Stopped tracking." << endl;
                        break;
                    case nite::SKELETON_CALIBRATING:
                        cout << "Calibrating..." << endl;
                        break;
                    case nite::SKELETON_TRACKED:
                        // cout << "Tracking!" << endl;
                        DrawSkeleton(&userTracker, user, imgToShow, skeletonFile);
                        break;
                    case nite::SKELETON_CALIBRATION_ERROR_NOT_IN_POSE:
                    case nite::SKELETON_CALIBRATION_ERROR_HANDS:
                    case nite::SKELETON_CALIBRATION_ERROR_LEGS:
                    case nite::SKELETON_CALIBRATION_ERROR_HEAD:
                    case nite::SKELETON_CALIBRATION_ERROR_TORSO:
                        cout << "Calibration Failed... :-|" << endl;
                        break;
                }
            }
        }

        cv::putText(imgToShow, recording ? "Recording" : "Not Recording", cv::Point(10, imgToShow.rows - 50), cv::FONT_HERSHEY_SIMPLEX, 5, Scalar(128), 5);

        cv::resize(imgToShow, imgToShow, cv::Size(), 0.5, 0.5);
        cvtColor(rgbmat, videomat, COLOR_RGB2BGR);
        cvtColor(imgToShow, imgToShow, COLOR_RGB2BGR);
        cv::imshow("rgb", imgToShow);

        if (recording) videowriter << videomat;

        int key = cv::waitKey(1);
        protonect_shutdown = protonect_shutdown || (key > 0 && ((key & 0xFF) == 27)); // shutdown on escape

        if (key > 0 && ((key & 0xFF) == 32)) {
            if (!recording) {
                videowriter.open("Saque/Actor 4/out" + to_string(recordIndex) + ".avi", CV_FOURCC('M', 'J', 'P', 'G'), 15, Size(1920, 1080), true);
                skeletonFile.open("Saque/Actor 4/out" + to_string(recordIndex++) + ".csv");
            }
            else {
                videowriter.release();
                skeletonFile.close();
            }

            recording = !recording; // toggle record
        }
    }

    cout << "Exit!!" << endl;

    //! [stop]
    openni::OpenNI::shutdown();
    //! [stop]

    std::cout << "Streaming Ends!" << std::endl;
    return 0;
}
