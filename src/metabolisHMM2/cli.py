import click
from .single_marker_search import single_marker_search as run_single_marker_search

@click.group()
def cli():
    """metabolisHMM2: Exploring genome annotations and phylogenies with HMM markers."""
    pass

@cli.command(name="marker-search")
@click.option('--input_dir', required=True, help='Directory containing input genomes.')
@click.option('--output_dir', required=True, help='Directory to store output files.')
@click.option('--markers_dir', required=True, help='Directory containing HMM marker files.')
@click.option('--threads', default=1, type=int, help='Number of threads to use.')
def run_single_marker_search_command(input_dir, output_dir, markers_dir, threads):
    """Search a single HMM marker against an input directory of genomes."""
    click.echo("Debug: single_marker_search function called")
    click.echo(f"Debug: input_dir={input_dir}")
    click.echo(f"Debug: output_dir={output_dir}")
    click.echo(f"Debug: markers_dir={markers_dir}")
    click.echo(f"Debug: threads={threads}")
    
    click.echo("Debug: About to call single_marker_search function")
    try:
        run_single_marker_search(input_dir, output_dir, markers_dir, threads)
        click.echo("Debug: marker-search completed successfully")
    except Exception as e:
        click.echo(f"Debug: Exception occurred: {str(e)}")
        click.echo("Debug: marker-search function failed")
        raise

if __name__ == '__main__':
    cli()