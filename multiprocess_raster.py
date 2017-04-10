import multiprocessing
import time
import subprocess

tile_list = ['00N_010E', '00N_020E', '00N_030E', '00N_040E']

def process_tile(tile_id):

    print 'downloading loss and extent for tile id {}'.format(tile_id)
    time.sleep(1)
    extent_url = r'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_treecover2000_{}.tif'.format(tile_id)
    loss_url = r'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2014/Hansen_GFC2014_lossyear_{}.tif'.format(tile_id)
    extent_local = r'data/{}_extent.tif'.format(tile_id)
    loss_local = r'data/{}_loss.tif'.format(tile_id)

    subprocess.check_call(['wget', '-O', extent_local, extent_url])
    subprocess.check_call(['wget', '-O', loss_local, loss_url])
    
    print 'writing combined tile for {}'.format(tile_id)
    encoded_tile = '{}_losstcd.tif'.format(tile_id)
    encode_tiles_cmd = ['./encode_hansen_loss_tcd.exe', extent_local, loss_local, encoded_tile]
    subprocess.check_call(encode_tiles_cmd)
    
    print 'uploading tile {} to s3'.format(tile_id)
    upload_cmd = ['aws', 's3', 'cp', encoded_tile, 's3://gfw2-data/forest_cover/loss_tcd_tiles/']
    subprocess.check_call(upload_cmd)


if __name__ == '__main__':
    count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=count)
    pool.map(process_tile, tile_list)
