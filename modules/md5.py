
def hashfile(file, hasher, blocksize=65536):
    """
    Esegue la funzione di hash sul contenuto del file per ottenere l'md5

    :param file: file su cui effettuare l'hash md5
    :type file: file
    :param hasher: componente che esegue l'hash
    :type hasher: object
    :param blocksize: dimensione del buffer di lettura del file
    :type blocksize: int
    :return: hash md5 del file
    :rtype: str
    """

    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
    return hasher.hexdigest()
