from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from .utils import check_dependencies, create_directory, run_command

from Bio import SeqIO
from Bio import SearchIO

def single_marker_search(input_dir, output_dir, marker_dir, threads):
    """Run single marker search on a directory of genomes."""
    check_dependencies()
    create_directory(output_dir)

    genomes = list(Path(input_dir).glob("*.fasta"))
    markers = list(Path(marker_dir).glob("*.hmm"))
    output_dir.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(process_genome, genome, output_dir, markers) for genome in genomes]
        for future in as_completed(futures):
            future.result()

def process_genome(genome, output_dir, markers):
    """Process a single genome with a list of markers."""
    genome_name = genome.stem
    # get proteins
    protein_file = run_prodigal(genome, output_dir, genome_name)
    # Run hmmsearch for each marker
    for marker in markers:
        run_hmmsearch(protein_file, marker, output_dir, genome_name)

def run_prodigal(genome, output_dir, genome_name):
    """Run Prodigal on a genome file and store the results in the output directory."""
    protein_file = Path(output_dir) / f"{genome_name}.proteins.fasta"
    command = [
        'prodigal',
        '-i', str(genome),
        '-a', str(protein_file),
        '-p', 'meta',
        '-q'
    ]
    run_command(command)
    return protein_file

def run_hmmsearch(protein_file, marker, output_dir, genome_name):
    """Run hmmsearch on a protein file and store the results in the output directory."""
    marker_name = marker.stem
    output_file = Path(output_dir) / f"{genome_name}_{marker_name}.out"
    command = [
        'hmmsearch',
        '--tblout', str(output_file),
        '--cut_tc',
        '--cpu', '1',
        str(marker),
        str(protein_file)
    ]
    run_command(command)
    parse_hmmsearch_output(output_file, protein_file, output_dir, genome_name, marker_name)

def parse_hmmsearch_output(hmmer_output, protein_file, output_dir, genome_name, marker_name):
    """Parse hmmsearch output, write hits to fasta, and summarize results."""
    hits_dict = {}
    for qresult in SearchIO.parse(hmmer_output, "hmmer3-tab"):
        query_name = qresult.id
        query_accession = qresult.accession
        for hit in qresult.hits:
            hit_id = hit.id
            evalue = hit.hsps[0].evalue
            hits_dict[hit_id] = (query_accession, query_name, evalue)

    hits_fasta = Path(output_dir) / f"{genome_name}_{marker_name}_hits.fasta"
    summary_file = Path(output_dir) / f"{genome_name}_{marker_name}_summary.txt"

    # Write hits to fasta file
    with open(hits_fasta, "w") as f:
        for record in SeqIO.parse(protein_file, "fasta"):
            if record.id in hits_dict:
                SeqIO.write(record, f, "fasta")

    # Summarize hits
    with open(summary_file, "w") as f:
        f.write("hit_id\tlength\te_value\tquery_accession\tquery_name\n")
        for record in SeqIO.parse(hits_fasta, "fasta"):
            hit_id = record.id
            length = len(record.seq)
            query_accession, query_name, evalue = hits_dict[hit_id]
            f.write(f"{hit_id}\t{length}\t{evalue}\t{query_accession}\t{query_name}\n")

if __name__ == "__main__":
    single_marker_search()