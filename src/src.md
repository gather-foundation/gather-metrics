# Source Code (src folder)

The src folder contains the source code for the project. This is where the main logic and components of the application are located. Organizing the project in this manner helps maintain a clean and well-structured codebase.

## Dependencies

Dependencies for the project should be installed at the appropriate level based on their scope.

For instance, when initializing an Angular project within the src folder, a separate package.json file will be generated inside the src folder. This is where you would install the dependencies specifically required by the Angular project.

On the other hand, tools like Commitizen, which are used for the entire repository, should be installed at the root level of the repository. In such cases, the dependencies will be listed in the package.json file located in the root folder of the repository.

By managing dependencies in this way, you can ensure that each part of the project has access to the necessary libraries and tools while maintaining a clear separation of concerns.
