from pathlib import Path

from ariadne import make_executable_schema

from mutation import mutation
from queries import query
from types import product_type, datetime_scalar, product_interface

schema = make_executable_schema(
    (Path(__file__).parent / 'products.graphql').read_text(),
    [query, mutation, product_type, datetime_scalar, product_interface]
)