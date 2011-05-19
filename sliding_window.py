from __future__ import division

import cv

from cvutils import *

def get_mask(w,h):
    img = cv.CreateImage((w,h), 8, 1)
    cv.Zero(img)
    t = int(w / 5)
    k = int(w / 15)
    p = w-k-1
    poly =( (k,t), (t+k,0), (p-t,0), (p,t),
            (p,h-t), (p-t, h), (t+k,h), (k,h-t))
    cv.FillPoly(img,(poly,), 255)
    return img

def samples_generator(img, w, h, slide_step=1, resize_step=1.2, bw_from_v_plane=True, withmask=False):
    img = prepare_bw(img,take_v_plane=bw_from_v_plane)
    ow, oh = sizeOf(img)
    if ow < w and oh < h:
        raise Exception("Requested sample is bigger than source")
    mask = get_mask(w,h)
    cw, ch = ow*resize_step, oh*resize_step
    boxy = cv.CreateImage((w,h),8,1)
    while cw > w and ch > h:
        ch /= resize_step
        cw /= resize_step

        k = ow / cw

        if cw < w or ch < h:
            cw,ch = w,h

        tmp = cv.CreateImage((cw,ch), 8, 1)
        cv.Resize(img, tmp)
        img = tmp

        for cx in range(0,cw-w+1,slide_step):
            for cy in range(0,ch-h+1,slide_step):
                cv.SetImageROI(img, (cx,cy,w,h))
                cv.Zero(boxy)
                cv.Copy(img, boxy)
                if withmask:
#                    To heavy to have mask
                    dst = cv.CreateImage((w,h), 8, 1)
                    cv.Zero(dst)
                    cv.Copy(img, dst, mask)
                yield boxy, (cx*k,cy*k,w*k,h*k)
        cv.ResetImageROI(img)

@time_took
def test_take_samples():
    path = "/Users/soswow/Documents/Face Detection/test/lenas"
    img = cv.LoadImage("sample/lena.bmp")
    sample_gen = samples_generator(img, 32, 32, slide_step=8, resize_step=1.6)
    for i, (sample,_) in enumerate(sample_gen):
        cv.SaveImage("%s/%d.png" % (path, i), sample)

def profile():
    import cProfile
    import pstats
    pass
#    cProfile.run('test_take_samples()', 'take_samples')
    p = pstats.Stats('take_samples')
    p.strip_dirs().sort_stats('cumulative').print_stats()

def main():
#    profile()
    test_take_samples()
#    img = get_mask(32, 32)
#    show_image(img)

if __name__ == "__main__":
    main()