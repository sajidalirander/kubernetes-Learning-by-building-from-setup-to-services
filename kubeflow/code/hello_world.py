import os
from kfp import dsl

# The @dsl.component decorator tells KFP that this function is a reusable component.
@dsl.component
def say_hello(name: str):
    """A simple component that prints a greeting."""
    print(f"Hello, {name}!")

# The @dsl.pipeline decorator defines the overall workflow.
@dsl.pipeline(
    name='hello-world-pipeline',
    description='A simple introductory pipeline.'
)
def my_first_pipeline(recipient: str = 'World'):
    """Our main pipeline that uses the say_hello component."""
    say_hello(name=recipient)

if __name__ == '__main__':
    from kfp import compiler
    filename_no_ext = os.path.splitext(os.path.basename(__file__))[0].replace("_", "-")
    compiler.Compiler().compile(my_first_pipeline, f'./kubeflow/kfp_yaml/{filename_no_ext}-pipeline.yaml')