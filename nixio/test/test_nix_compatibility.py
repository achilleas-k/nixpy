# Copyright (c) 2017, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
import os
import numpy as np
import nixio as nix


def test_blocks(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    for idx in range(10):
        blk = nix_file.create_block("test_block" + str(idx),
                                    "blocktype")
        blk.definition = "definition block " + str(idx)
        blk.force_created_at(np.random.randint(1000000000))

    nix_file.close()


def test_groups(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("test_block", "blocktype")
    for idx in range(12):
        grp = blk.create_group("group_" + str(idx), "grouptype")
        grp.definition = "group definition " + str(idx*10)
        grp.force_created_at(np.random.randint(1000000000))

    nix_file.close()


def test_data_arrays(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "blocktype")
    grp = blk.create_group("testgroup", "grouptype")

    for idx in range(7):
        da = blk.create_data_array("data_" + str(idx), "thedata",
                                   data=np.random.random(40))
        da.definition = "da definition " + str(sum(da[:]))
        da.force_created_at(np.random.randint(1000000000))
        da.label = "data label " + str(idx)
        da.unit = "mV"

        if (idx % 2) == 0:
            da.expansion_origin = np.random.random()*100
            grp.data_arrays.append(da)
        if (idx % 3) == 0:
            da.polynom_coefficients = tuple(np.random.random(3))

    nix_file.close()


def test_tags(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "blocktype")
    grp = blk.create_group("testgroup", "grouptype")

    for idx in range(16):
        tag = blk.create_tag("tag_" + str(idx), "atag",
                             np.random.random(idx*2))
        tag.definition = "tag def " + str(idx)
        tag.extent = np.random.random(idx*2)

        tag.units = ["mV", "s"]
        tag.force_created_at(np.random.randint(100000000))

        if (idx % 3) == 0:
            grp.tags.append(tag)

    nix_file.close()


def test_multi_tags(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "blocktype")
    grp = blk.create_group("testgroup", "grouptype")

    for idx in range(11):
        posda = blk.create_data_array("pos_" + str(idx), "positions",
                                      data=np.random.random(idx*10))
        extda = blk.create_data_array("ext_" + str(idx), "extents",
                                      data=np.random.random(idx*10))
        mtag = blk.create_multi_tag("mtag_" + str(idx), "some multi tag",
                                    posda)
        mtag.extents = extda

        if (idx % 2) == 0:
            grp.multi_tags.append(mtag)

    nix_file.close()


def test_sources(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "sourcetest")
    grp = blk.create_group("testgroup", "sourcetest")
    da = blk.create_data_array("da", "sourcetest",
                               data=np.random.random(10))
    pos = blk.create_data_array("pos", "sourcetest",
                                data=np.random.random(10))
    mtag = blk.create_multi_tag("mtag", "sourcetest", pos)
    grp.data_arrays.append(da)

    for idx in range(20):
        src = blk.create_source("src" + str(idx), "source")
        src_child = src.create_source("child src " + str(idx), "source")

        if (idx % 5) == 0:
            grp.sources.append(src)

        if (idx % 3) == 0:
            mtag.sources.append(src_child)

        if (idx % 8) == 0:
            da.sources.append(src)

    # TODO: Nested sources

    nix_file.close()


def test_dimensions(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "dimtest")

    da_set = blk.create_data_array("da with set", "datype",
                                   data=np.random.random(20))
    da_set.append_set_dimension()
    da_set.dimensions[0].labels = ["label one", "label two"]

    da_range = blk.create_data_array("da with range", "datype",
                                     data=np.random.random(12))
    rngdim = da_range.append_range_dimension(np.random.random(12))
    rngdim.label = "range dim label"
    rngdim.unit = "ms"

    da_sample = blk.create_data_array("da with sample", "datype",
                                      data=np.random.random(10))
    smpldim = da_sample.append_sampled_dimension(0.3)
    smpldim.offset = 0.1
    smpldim.unit = "mV"

    da_sample.dimensions[0].label = "sample dim label"

    da_alias = blk.create_data_array("da with alias", "datype",
                                     data=np.random.random(19))
    da_alias.unit = "F"
    da_alias.label = "fee fi fo fum"
    da_alias.append_alias_range_dimension()

    da_multi_dim = blk.create_data_array("da with multiple", "datype",
                                         data=np.random.random(30))
    da_multi_dim.append_sampled_dimension(0.1)
    da_multi_dim.append_set_dimension()
    da_multi_dim.append_range_dimension(np.random.random(10))

    nix_file.close()


def test_tag_features(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "feattest")
    da_ref = blk.create_data_array("da for ref", "datype",
                                   nix.DataType.Double,
                                   data=np.random.random(15))
    da_ref.append_sampled_dimension(0.2)
    tag_feat = blk.create_tag("tag for feat", "tagtype", [2])
    tag_feat.references.append(da_ref)

    linktypes = [nix.LinkType.Tagged, nix.LinkType.Untagged,
                 nix.LinkType.Indexed]
    for idx in range(6):
        da_feat = blk.create_data_array("da for feat " + str(idx),
                                        "datype", nix.DataType.Float,
                                        data=np.random.random(12))
        da_feat.append_sampled_dimension(1.0)
        tag_feat.create_feature(da_feat, linktypes[idx % 3])

    nix_file.close()


def test_multi_tag_features(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    blk = nix_file.create_block("testblock", "mtfeattest")
    index_data = blk.create_data_array(
        "indexed feature data", "test",
        dtype=nix.DataType.Double, shape=(10, 10)
    )
    dim1 = index_data.append_sampled_dimension(1.0)
    dim1.unit = "ms"
    dim2 = index_data.append_sampled_dimension(1.0)
    dim2.unit = "ms"

    data1 = np.zeros((10, 10))
    value = 0.0
    total = 0.0
    for i in range(10):
        value = 100 * i
        for j in range(10):
            value += 1
            data1[i, j] = value
            total += data1[i, j]

    index_data[:, :] = data1

    tagged_data = blk.create_data_array(
        "tagged feature data", "test",
        dtype=nix.DataType.Double, shape=(10, 20, 10)
    )
    dim1 = tagged_data.append_sampled_dimension(1.0)
    dim1.unit = "ms"
    dim2 = tagged_data.append_sampled_dimension(1.0)
    dim2.unit = "ms"
    dim3 = tagged_data.append_sampled_dimension(1.0)
    dim3.unit = "ms"

    data2 = np.zeros((10, 20, 10))
    for i in range(10):
        value = 100 * i
        for j in range(20):
            for k in range(10):
                value += 1
                data2[i, j, k] = value

    tagged_data[:, :, :] = data2

    event_labels = ["event 1", "event 2"]
    dim_labels = ["dim 0", "dim 1", "dim 2"]
    event_array = blk.create_data_array("positions", "test",
                                        data=np.random.random((2, 3)))
    extent_array = blk.create_data_array("extents", "test",
                                         data=np.random.random((2, 3)))
    extent_set_dim = extent_array.append_set_dimension()
    extent_set_dim.labels = event_labels
    extent_set_dim = extent_array.append_set_dimension()
    extent_set_dim.labels = dim_labels

    feature_tag = blk.create_multi_tag("feature_tag", "events",
                                       event_array)
    data_array = blk.create_data_array("featureTest", "test",
                                       nix.DataType.Double, (2, 10, 5))
    data = np.random.random((2, 10, 5))
    data_array[:, :, :] = data

    feature_tag.extents = extent_array

    feature_tag.create_feature(index_data, nix.LinkType.Indexed)
    feature_tag.create_feature(tagged_data, nix.LinkType.Tagged)
    feature_tag.create_feature(index_data, nix.LinkType.Untagged)

    nix_file.close()


def test_multi_tag_references(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    interval = 0.001
    x = np.arange(0, 10, interval)
    y = np.sin(2*np.pi*x)
    blk = nix_file.create_block("blk", "reftest")
    da = blk.create_data_array("sin", "data", data=y)
    da.unit = "dB"
    dim = da.append_sampled_dimension(interval)
    dim.unit = "s"

    pos = blk.create_data_array("pos1", "positions", data=np.array([[0]]))
    pos.append_set_dimension()
    pos.append_set_dimension()
    pos.unit = "ms"
    ext = blk.create_data_array("ext1", "extents",
                                data=np.array([[2000]]))
    ext.append_set_dimension()
    ext.append_set_dimension()
    ext.unit = "ms"

    mtag = blk.create_multi_tag("sin1", "tag", pos)
    mtag.extents = ext
    mtag.units = ["ms"]
    mtag.references.append(da)

    nix_file.close()


def test_properties(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    sec = nix_file.create_section("test section", "proptest")
    sec.create_property("test property", nix.Value(0))
    sec.create_property("test str", nix.DataType.String)
    sec.create_property("other property", nix.DataType.Int64)

    sec.create_property("prop Int32", nix.DataType.Int32)
    sec.create_property("prop Int64", nix.DataType.Int64)
    sec.create_property("prop UInt32", nix.DataType.UInt32)
    sec.create_property("prop UInt64", nix.DataType.UInt64)
    sec.create_property("prop Float", nix.DataType.Float)
    sec.create_property("prop Double", nix.DataType.Double)
    sec.create_property("prop String", nix.DataType.String)
    sec.create_property("prop Bool", nix.DataType.Bool)

    sec.props[0].mapping = "mapping"
    sec.props[1].definition = "def"

    sec.props[0].values = [nix.Value(101)]
    sec.props[1].values = [nix.Value("foo"), nix.Value("bar"),
                           nix.Value("baz")]
    sec.props["prop Float"].values = [nix.Value(10.0), nix.Value(33.3),
                                      nix.Value(1.345), nix.Value(90.2)]

    nix_file.close()


def test_sections(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    for idx in range(30):
        sec = nix_file.create_section("test section" + str(idx),
                                      "sectiontest")
        sec.definition = "sec definition " + str(idx)
        sec.mapping = "sec mapping " + str(idx)
        sec.repository = "sec repo" + str(idx * 3)

        nested_sec = sec.create_section("nested_section", "sec")
        if (idx % 3) == 0:
            lvl2 = nested_sec.create_section("level 2", "sec")

            if (idx % 12) == 0:
                lvl2.create_section("level 3", "sec")

    block = nix_file.create_block("block", "section test")
    block.metadata = nix_file.sections[0].sections[0].sections[0]

    nix_file.close()


def test_file(tmpdir):
    nixfilepath = os.path.join(tmpdir, "blocktest.nix")
    nix_file = nix.File.open(nixfilepath, mode=nix.FileMode.Overwrite,
                             backend="h5py")
    print(nix_file.version)
