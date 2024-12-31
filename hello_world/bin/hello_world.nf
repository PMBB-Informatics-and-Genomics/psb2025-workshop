workflow {
    greeting_list = ['Hello', 'Hola', 'Bonjour', 'Ciao']
    many_hellos = Channel.fromList(greeting_list)

    // greetings_stdout is another Channel!
    greetings_stdout = say_hello(many_hellos)
    greetings_stdout | view
}

process say_hello {
    input:
        val(greeting)
    output:
        stdout
    shell:
        """
        echo "${greeting}, World!"
        """
}
