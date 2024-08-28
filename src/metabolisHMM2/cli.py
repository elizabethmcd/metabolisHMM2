import click
from .single_marker_search import single_marker_search

@click.group()
def cli():
    """metabolisHMM2: Exploring genome annotations and phylogenies with HMM markers."""
    pass

@cli.command()
@click.option('--input-dir', required=True, help='Directory containing input genomes.')
@click.option('--output-dir', required=True, help='Directory to store output files.')
@click.option('--markers-dir', required=True, help='Directory containing HMM marker files.')
@click.option('--threads', default=1, type=int, help='Number of threads to use.')
def single_marker_search(input_dir, output_dir, markers_dir, threads):
    """Search a single HMM marker against an input directory of genomes."""
    single_marker_search(input_dir, output_dir, markers_dir, threads)

    click.echo(f"Running metabolisHMM2 with:")
    click.echo(f"Input directory: {input_dir}")
    click.echo(f"Output directory: {output_dir}")
    click.echo(f"Markers directory: {markers_dir}")
    click.echo(f"Threads: {threads}")

if __name__ == '__main__':
    cli()