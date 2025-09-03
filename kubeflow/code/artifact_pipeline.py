import os
from kfp import dsl
from kfp.dsl import Input, Output, Dataset

@dsl.component
def create_file(text_to_write: str, output_artifact: Output[Dataset]):
    """Creates a text file with some content."""
    # The .path attribute gives us the actual file path to write to.
    # KFP manages creating this path for us.
    with open(output_artifact.path, 'w') as f:
        f.write(text_to_write)
    print(f"Successfully created file with content: '{text_to_write}'")

@dsl.component
def read_file(input_artifact: Input[Dataset]):
    """Reads the content of an input file and prints it."""
    # The .path attribute gives us the actual file path to read from.
    # KFP automatically downloads the artifact and provides this path.
    with open(input_artifact.path, 'r') as f:
        content = f.read()
    print(f"Read file and found content: '{content}'")

@dsl.pipeline(
    name='artifact-passing-pipeline',
    description='A pipeline that passes a file between components.'
)
def my_artifact_pipeline(message: str = 'Hello from an artifact stored in MinIO!'):
    """Our main pipeline that creates and then reads a file."""
    create_task = create_file(text_to_write=message)
    # We pass the output of the first task as the input to the second.
    read_file(input_artifact=create_task.output)


if __name__ == '__main__':
    from kfp import compiler
    filename_no_ext = os.path.splitext(os.path.basename(__file__))[0].replace("_", "-")
    compiler.Compiler().compile(my_artifact_pipeline, f'./kubeflow/kfp_yaml/{filename_no_ext}-pipeline.yaml')