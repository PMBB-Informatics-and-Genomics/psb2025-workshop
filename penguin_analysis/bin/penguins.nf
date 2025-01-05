#!/usr/bin/env nextflow

params.data = '/home/zach/projects/pmbb/psb2025-workshop/penguin_analysis/data/penguins_size.csv'
params.cleaning_script = '/home/zach/projects/pmbb/psb2025-workshop/penguin_analysis/bin/data_cleaning.py'
params.analysis_script = '/home/zach/projects/pmbb/psb2025-workshop/penguin_analysis/bin/species_analysis.py'

process clean_data {
    publishDir "${launchDir}/data/"
    input:
        path cleaning_script
        path raw_input
        
    output:
        path 'penguins_cleaned.csv'
        
    script:
    """
    python  ${cleaning_script} --input_file ${raw_input}
    """
}

process species_analysis {
    publishDir "${launchDir}/results/"
    input:
        val species
        path analysis_script
        path cleaned_data
        
    output:
        path "${species}_basic_stats.csv"
        path "${species}_correlations.png"
        path "${species}_dimorphism_stats.csv"
        path "${species}_distributions.png"
    
    script:
        """
        python ${analysis_script} --input_file ${cleaned_data} --species ${species} 
        """
}


workflow {
    // create a species channel
    species_channel = Channel.from('Adelie', 'Gentoo', 'Chinstrap')
    raw_data = "${params.data}"
    
    // clean the data
    cleaning_script = "${params.cleaning_script}"
    cleaned_data = clean_data(cleaning_script, raw_data)
    
    // run the analysis
    analysis_script = "${params.analysis_script}"
    species_analysis(species_channel, analysis_script, cleaned_data)
}
