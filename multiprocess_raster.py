import multiprocessing
import time
import subprocess

tile_list = ['00N_000E', '00N_010E', '00N_020E', '00N_030E', '00N_040E']

def process_tile(tile_id):

    print 'downloading loss and extent for tile id {}'.format(tile_id)
    time.sleep(1)
        
    print 'writing combined tile for {}'.format(tile_id)
    time.sleep(5)
    
    print 'uploading tile {} to s3'.format(tile_id)
    time.sleep(1)


if __name__ == '__main__':
    count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=count)
    pool.map(process_tile, tile_list)