# About

Deployment package dependencies does not play nice with API dependencies. Thus, lives in a separate folder.

# Known issues

- [If your cluster runs on non-x86_64 architecture (e.g., Apple Silicon), your image must be built natively for that architecture. Otherwise, your job may get stuck at Start streaming logs.](https://github.com/skypilot-org/skypilot/issues/3035)