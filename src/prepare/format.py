
width = 800
height = 600
depth = 3
def annotation(img,data):
    xml_name = str(img).split('.',1)[0] + '.xml'
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('VOC2014_instance'),
        E.filename(img),
        E.source(
            E.database('COCO'),
            E.annotation('COCO'),
            E.image('COCO'),
            E.url(img)
        ),
        E.size(
            E.width(width),
            E.height(height),
            E.depth(depth)
        ),
        E.segmented(0),
    )
    for i in data: #i[0], i[1][0],i[1][1],i[1][2],i[1][3]
        E2 = objectify.ElementMaker(annotate=False)
        anno_tree2 = E2.object(
            E.name(i[0]),
            E.bndbox(
                E.xmin(i[1][0]),
                E.ymin(i[1][1]),
                E.xmax(i[1][2]),
                E.ymax(i[1][3])
            ),
            E.difficult(0)
        )

        anno_tree.append(anno_tree2)
    etree.ElementTree(anno_tree).write('/usr/local/xml/'+xml_name, pretty_print=True)

if __name__ == '__main__':
    pass