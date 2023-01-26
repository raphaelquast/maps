import matplotlib as mpl

mpl.rcParams["toolbar"] = "None"

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import unittest

import pandas as pd
import numpy as np

from eomaps import Maps, MapsGrid

from matplotlib.backend_bases import MouseEvent, KeyEvent


def button_press_event(canvas, x, y, button, dblclick=False, guiEvent=None):
    canvas._button = button
    s = "button_press_event"
    mouseevent = MouseEvent(
        s, canvas, x, y, button, canvas._key, dblclick=dblclick, guiEvent=guiEvent
    )
    canvas.callbacks.process(s, mouseevent)


def button_release_event(canvas, x, y, button, guiEvent=None):
    s = "button_release_event"
    event = MouseEvent(s, canvas, x, y, button, canvas._key, guiEvent=guiEvent)
    canvas.callbacks.process(s, event)
    canvas._button = None


def motion_notify_event(canvas, x, y, guiEvent=None):
    s = "motion_notify_event"
    event = MouseEvent(s, canvas, x, y, guiEvent=guiEvent)
    canvas.callbacks.process(s, event)


def scroll_event(canvas, x, y, step, guiEvent=None):
    s = "scroll_event"
    event = MouseEvent(s, canvas, x, y, step=step, guiEvent=guiEvent)
    canvas.callbacks.process(s, event)


def key_press_event(canvas, key, guiEvent=None):
    s = "key_press_event"
    event = KeyEvent(s, canvas, key, guiEvent=guiEvent)
    canvas.callbacks.process(s, event)


def key_release_event(canvas, key, guiEvent=None):
    s = "key_release_event"
    event = KeyEvent(s, canvas, key, guiEvent=guiEvent)
    canvas.callbacks.process(s, event)
    canvas._key = None


class TestBasicPlotting(unittest.TestCase):
    def setUp(self):
        x, y = np.meshgrid(
            np.linspace(-19000000, 19000000, 50), np.linspace(-19000000, 19000000, 50)
        )
        x, y = x.ravel(), y.ravel()

        self.data = pd.DataFrame(dict(x=x, y=y, value=y - x))

    def test_simple_map(self):
        m = Maps(4326)
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)
        m.plot_map()
        plt.close(m.f)

        # -------------------------------------

        m = Maps()
        m.add_feature.preset.ocean()
        m.add_feature.preset.coastline()
        m.set_data_specs(
            data=self.data, x="x", y="y", crs=3857, cpos="ur", cpos_radius=1
        )
        m.plot_map()
        m.indicate_extent(20, 10, 60, 76, crs=4326, fc="r", ec="k", alpha=0.5)
        plt.close(m.f)

    def test_simple_plot_shapes(self):
        usedata = self.data.sample(500)

        # rectangles
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_shape.geod_circles(radius=100000)
        m.set_classify.Quantiles(k=5)
        m.plot_map(indicate_masked_points=True)

        m.add_feature.preset.ocean(ec="k", scale="110m")
        plt.close("all")

        # rectangles
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_classify.EqualInterval(k=5)
        m.set_shape.rectangles()
        m.plot_map(indicate_masked_points=True)
        m.add_feature.preset.ocean(ec="k", scale="110m")

        m2 = m.new_layer()
        m2.inherit_data(m)
        m2.set_shape.rectangles(radius=1, radius_crs=4326)
        m2.plot_map(ec="k", indicate_masked_points=True)

        m3 = m.new_layer()
        m3.inherit_data(m)
        m3.inherit_classification(m)
        m3.set_shape.rectangles(radius=(0.5, 2), radius_crs="out")
        m3.plot_map(ec="k", indicate_masked_points=True)

        r = usedata.x.rank()
        r = r / r.max() * 10
        m4 = m.new_layer()
        m4.inherit_data(m)
        m4.set_shape.rectangles(radius=r, radius_crs="out")
        m4.plot_map(ec="k", fc="none", indicate_masked_points=True)

        plt.close("all")

        # rectangles
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_shape.rectangles(mesh=True)
        m.plot_map(indicate_masked_points=True)

        m2 = m.new_layer()
        m2.inherit_data(m)
        m2.set_shape.rectangles(radius=1, radius_crs=4326, mesh=True)
        m2.plot_map()

        m3 = m.new_layer()
        m3.inherit_data(m)
        m3.set_shape.rectangles(radius=(1, 2), radius_crs="out", mesh=True)
        m3.plot_map(indicate_masked_points=True)

        plt.close("all")

        # ellipses
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_shape.ellipses()
        m.plot_map(indicate_masked_points=True)

        m2 = m.new_layer()
        m2.inherit_data(m)
        m2.inherit_classification(m)
        m2.set_shape.ellipses(radius=1, radius_crs=4326)
        m2.plot_map()

        m3 = m.new_layer()
        m3.inherit_data(m)
        m3.inherit_classification(m)

        r = usedata.x.rank()
        r = r / r.max() * 10
        m3.set_shape.ellipses(radius=r, radius_crs="out")
        m3.plot_map(ec="k", fc="none", indicate_masked_points=True)

        plt.close("all")

        # scatter_points
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_shape.scatter_points(marker="*", size=20)
        m.plot_map()

        m2 = m.new_layer()
        m2.inherit_data(m)
        m2.set_shape.scatter_points(size=1)
        m2.plot_map(indicate_masked_points=True)

        m3 = m.new_layer()
        m3.inherit_data(m)
        r = usedata.x.rank()
        r = r / r.max() * 50
        m3.set_shape.scatter_points(size=r, marker="s")
        m3.plot_map(ec="k", fc="none", indicate_masked_points=True)

        plt.close("all")

        # delaunay
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_shape.delaunay_triangulation(flat=True)
        m.plot_map(indicate_masked_points=True)

        m2 = m.new_layer()
        m2.inherit_data(m)
        m2.set_shape.delaunay_triangulation(flat=False)
        m2.plot_map(indicate_masked_points=True)

        m3 = m.new_layer()
        m3.inherit_data(m)
        m3.set_shape.delaunay_triangulation(masked=False)
        m3.plot_map()

        plt.close("all")

        # voronoi
        m = Maps(4326)
        m.set_data(usedata, x="x", y="y", crs=3857)
        m.set_shape.voronoi_diagram(masked=False)
        m.plot_map(indicate_masked_points=True)

        m2 = m.new_layer()
        m2.inherit_data(m)
        m2.set_shape.voronoi_diagram(masked=True, mask_radius=5)
        m2.plot_map()

        plt.close("all")

    def test_cpos(self):
        m = Maps(4326)

        for cpos, color in zip(["ul", "ur", "ll", "lr", "c"], "rgbcm"):
            m2 = m.new_layer()
            m2.set_shape.ellipses(n=100)
            m2.set_data(
                self.data,
                x="x",
                y="y",
                crs=3857,
                cpos_radius=387755 / 2,
                cpos=cpos,
            )
            m2.plot_map(fc="none", ec=color, lw=0.5 if cpos != "c" else 2)

        plt.close(m.f)

    def test_alpha_and_splitbins(self):
        m = Maps(4326)
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)
        m.set_shape.rectangles()
        m.set_classify_specs(scheme="Percentiles", pct=[0.1, 0.2])

        m.plot_map(alpha=0.4)

        plt.close(m.f)

    def test_classification(self):
        m = Maps(4326)
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)
        m.set_shape.rectangles(radius=1, radius_crs="out")

        m.set_classify_specs(scheme="Quantiles", k=5)

        m.plot_map()

        plt.close(m.f)

    def test_add_callbacks(self):
        m = Maps(3857, layer="layername")
        m.data = self.data.sample(10)
        m.set_data_specs(x="x", y="y", crs=3857)
        m.set_shape.ellipses(radius=200000)

        m.plot_map()

        # attach all pick callbacks
        for n, cb in enumerate(m.cb.pick._cb_list):
            if n == 1:
                mouse_button = 1
                double_click = False
                modifier = "a"
            elif n == 2:
                mouse_button = 2
                double_click = False
                modifier = "b"
            else:
                mouse_button = 1
                double_click = True
                modifier = None

            cbID = m.cb.pick.attach(
                cb, double_click=double_click, button=mouse_button, modifier=modifier
            )
            self.assertTrue(
                cbID
                == f"{cb}_0__{m.layer}__{'double' if double_click else 'single'}__{mouse_button}__{modifier}"
            )
            self.assertTrue(len(m.cb.pick.get.attached_callbacks) == 1)
            m.cb.pick.remove(cbID)
            self.assertTrue(len(m.cb.pick.get.attached_callbacks) == 0)

        # attach all click callbacks
        for n, cb in enumerate(m.cb.click._cb_list):
            if n == 1:
                mouse_button = 1
                double_click = False
                modifier = "a"
            elif n == 2:
                mouse_button = 2
                double_click = False
                modifier = "b"
            else:
                mouse_button = 1
                double_click = True
                modifier = None

            cbID = m.cb.click.attach(
                cb, double_click=double_click, button=mouse_button, modifier=modifier
            )

            self.assertTrue(
                cbID
                == f"{cb}_0__{m.layer}__{'double' if double_click else 'single'}__{mouse_button}__{modifier}"
            )
            self.assertTrue(len(m.cb.click.get.attached_callbacks) == 1)
            m.cb.click.remove(cbID)
            self.assertTrue(len(m.cb.click.get.attached_callbacks) == 0)

        # attach all keypress callbacks
        double_click, mouse_button = True, 1
        for n, cb in enumerate(m.cb.keypress._cb_list):
            if n == 1:
                key = "x"
            if n == 2:
                key = "y"
            else:
                key = "z"

            cbID = m.cb.keypress.attach(cb, key=key)

            self.assertTrue(cbID == f"{cb}_0__{m.layer}__{key}")
            self.assertTrue(len(m.cb.keypress.get.attached_callbacks) == 1)
            m.cb.keypress.remove(cbID)
            self.assertTrue(len(m.cb.keypress.get.attached_callbacks) == 0)

        plt.close(m.f)

    def test_add_annotate(self):
        m = Maps()
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)

        m.plot_map()

        m.add_annotation(ID=m.data["value"].idxmax(), fontsize=15, text="adsf")

        def customtext(m, ID, val, pos, ind):
            return f"{m.data_specs}\n {val}\n {pos}\n {ID} \n {ind}"

        m.add_annotation(ID=m.data["value"].idxmin(), text=customtext)

        m.add_annotation(
            xy=(m.data.x[0], m.data.y[0]), xy_crs=3857, fontsize=15, text="adsf"
        )

        plt.close(m.f)

    def test_add_marker(self):
        crs = Maps.CRS.Orthographic(central_latitude=45, central_longitude=45)
        m = Maps(crs)
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)
        m.plot_map(set_extent=True)

        m.add_marker(
            np.arange(1810, 1840, 1),
            facecolor=[1, 0, 0, 0.5],
            edgecolor="r",
            shape="ellipses",
        )

        m.add_marker(
            np.arange(1810, 1840, 1),
            facecolor="none",
            edgecolor="k",
            shape="geod_circles",
            radius=300000,
        )

        m.add_marker(
            np.arange(1710, 1740, 1),
            facecolor=[1, 0, 0, 0.5],
            edgecolor="r",
            shape="rectangles",
        )

        m.add_marker(
            np.arange(1410, 1440, 1),
            facecolor=[1, 0, 0, 0.5],
            edgecolor="r",
            radius=50000,
            radius_crs="in",
        )

        m.add_marker(
            1630,
            facecolor=[1, 0, 0, 0.5],
            edgecolor="r",
            radius=2500000,
            shape="rectangles",
        )
        m.add_marker(
            1630, facecolor="none", edgecolor="k", linewidth=3, buffer=3, linestyle="--"
        )

        for r in [5, 10, 15, 20]:
            m.add_marker(
                1635, fc="none", ec="y", ls="--", radius=r, radius_crs=4326, lw=2
            )

        for r in np.linspace(10000, 1000000, 10):
            m.add_marker(
                1635, fc="none", ec="b", ls="--", radius=r, lw=2, shape="geod_circles"
            )

        for x in np.linspace(5000000, 6000000, 10):
            m.add_marker(
                xy=(x, 4000000),
                xy_crs="out",
                facecolor="none",
                edgecolor="r",
                radius=1000000,
                radius_crs="out",
            )

        m.add_marker(
            xy=(5040816, 4265306), facecolor="none", edgecolor="c", radius=800000, lw=5
        )

        m.add_marker(
            xy=(m.data.x[10], m.data.y[10]),
            xy_crs=3857,
            facecolor="none",
            edgecolor="r",
            radius="pixel",
            buffer=5,
        )

        for shape in ["ellipses", "rectangles"]:
            m.add_marker(
                1232, facecolor="none", edgecolor="r", radius="pixel", shape=shape, lw=2
            )

        plt.close(m.f)

    def test_copy(self):
        m = Maps(3857)
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)

        m.set_classify_specs(scheme="Quantiles", k=5)

        m2 = m.copy()

        self.assertTrue(
            m2.data_specs[["x", "y", "parameter", "crs"]]
            == {"x": "lon", "y": "lat", "parameter": None, "crs": 4326}
        )
        self.assertTrue([*m.classify_specs] == [*m2.classify_specs])
        self.assertTrue(m2.data == None)

        m3 = m.copy(data_specs=True)

        self.assertTrue(
            m.data_specs[["x", "y", "parameter", "crs"]]
            == m3.data_specs[["x", "y", "parameter", "crs"]]
        )
        self.assertTrue([*m.classify_specs] == [*m3.classify_specs])
        self.assertFalse(m3.data is m.data)
        self.assertTrue(m3.data.equals(m.data))

        m3.plot_map()
        plt.close(m3.f)

    def test_copy_connect(self):
        m = Maps(3857)
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857)
        m.set_shape.rectangles()
        m.set_classify_specs(scheme="Quantiles", k=5)
        m.plot_map()

        # plot on the same axes
        m2 = m.copy(data_specs=True, ax=m.ax)
        m2.set_shape.ellipses()
        m2.plot_map(facecolor="none", edgecolor="r")

        plt.close("all")

    def test_new_layer(self):
        m = Maps()
        m.add_feature.preset.ocean()
        m2 = m.new_layer()
        m2.add_feature.preset.land()

        m3 = m.new_layer()
        m3.add_feature.preset.coastline()

        m.fetch_layers()

        plt.close("all")

    def test_join_limits(self):
        mg = MapsGrid(2, 1, crs=3857)
        mg.add_feature.preset.coastline()
        mg.set_data(data=self.data, x="x", y="y", crs=3857)
        for m in mg:
            m.plot_map()

        mg.join_limits()

        mg.m_0_0.ax.set_extent((-20, 20, 60, 80))

        plt.close("all")

    def test_prepare_data(self):
        m = Maps()
        m.data = self.data
        m.set_data_specs(x="x", y="y", crs=3857, parameter="value")
        data = m._prepare_data()

    def test_layout_editor(self):

        mgrid = MapsGrid(2, 2, crs=[[4326, 4326], [3857, 3857]])

        for m in mgrid:
            m.add_feature.preset.coastline()
        mgrid.parent._layout_editor._make_draggable()
        mgrid.parent._layout_editor._undo_draggable()

        m = Maps()
        m.add_feature.preset.coastline()
        m._layout_editor._make_draggable()
        m._layout_editor._undo_draggable()

    def test_add_colorbar(self):
        gs = GridSpec(2, 2)

        m = Maps(ax=gs[0, 0])
        m.set_data_specs(data=self.data, x="x", y="y", crs=3857)
        m.plot_map()
        cb1 = m.add_colorbar(
            gs[1, 0],
            orientation="horizontal",
        )
        self.assertTrue(len(m._colorbars) == 1)
        self.assertTrue(m.colorbar is cb1)

        cb2 = m.add_colorbar(gs[0, 1], orientation="vertical")
        self.assertTrue(len(m._colorbars) == 2)
        self.assertTrue(m.colorbar is cb2)

        cb3 = m.add_colorbar(
            gs[1, 1],
            orientation="horizontal",
            hist_kwargs=dict(density=True),
            label="naseawas",
            hist_bins=5,
            extend_frac=0.4,
        )
        self.assertTrue(len(m._colorbars) == 3)
        self.assertTrue(m.colorbar is cb3)

        cb4 = m.add_colorbar(
            0.2,
            orientation="horizontal",
            hist_kwargs=dict(density=True),
            log=True,
            label="naseawas",
            out_of_range_vals="clip",
            hist_bins=5,
            extend_frac=0.4,
        )
        self.assertTrue(len(m._colorbars) == 4)
        self.assertTrue(m.colorbar is cb4)

        cb4.remove()
        self.assertTrue(len(m._colorbars) == 3)

        cb4 = m.add_colorbar(
            (0.1, 0.1, 0.7, 0.2),
            inherit_position=False,
            orientation="horizontal",
            hist_kwargs=dict(density=False),
            label="naseawas",
            out_of_range_vals="mask",
            hist_bins=5,
            extend_frac=0.4,
            show_outline=dict(color="r", lw=4),
        )
        self.assertTrue(len(m._colorbars) == 4)
        self.assertTrue(m.colorbar is cb4)

        m2 = m.new_layer("asdf")
        m2.set_data_specs(data=self.data, x="x", y="y", crs=3857)
        m2.set_classify.Quantiles(k=4)
        m2.plot_map()
        cb5 = m2.add_colorbar()

        m.redraw()

        self.assertTrue(all(cb.ax_cb.get_visible() for cb in m._colorbars))
        self.assertFalse(m2.colorbar.ax_cb.get_visible())
        m.show_layer("asdf")
        self.assertTrue(m2.colorbar.ax_cb.get_visible())

        self.assertTrue(len(m2._colorbars) == 1)
        self.assertTrue(all(not cb.ax_cb.get_visible() for cb in m._colorbars))

        self.assertTrue(m2.colorbar is cb5)

        # test setting custom bins
        bins = [-5e6, 5e6, 1e7]
        labels = ["A", "b", "c", "d"]
        m3 = m.new_layer("asdf")
        m3.set_data_specs(data=self.data, x="x", y="y", crs=3857)
        m3.set_classify.UserDefined(bins=bins)
        m3.plot_map()
        cb6 = m3.add_colorbar()
        cb6.set_bin_labels(bins, labels)
        m.show_layer(m3.layer)

        self.assertTrue(labels == [i.get_text() for i in cb6.ax_cb.get_xticklabels()])

        cb6.set_bin_labels(bins, labels, show_values=True)
        cb6.tick_params(which="minor", rotation=90)

    def test_MapsGrid(self):
        mg = MapsGrid(2, 2, crs=4326)
        mg.set_data(
            data=self.data, x="x", y="y", crs=3857, encoding=dict(scale_factor=1e-7)
        )
        mg.set_classify_specs(scheme=Maps.CLASSIFIERS.EqualInterval, k=4)
        mg.set_shape.rectangles()
        mg.plot_map()

        mg.add_annotation(ID=520)
        mg.add_marker(ID=5, fc="r", radius=10, radius_crs=4326)
        mg.add_colorbar()
        self.assertTrue(mg.m_0_0 is mg[0, 0])
        self.assertTrue(mg.m_0_1 is mg[0, 1])
        self.assertTrue(mg.m_1_0 is mg[1, 0])
        self.assertTrue(mg.m_1_1 is mg[1, 1])

        plt.close(mg.f)

    def test_MapsGrid2(self):
        mg = MapsGrid(
            2,
            2,
            m_inits={"a": (0, slice(0, 2)), 2: (1, 0)},
            crs={"a": 4326, 2: 3857},
            ax_inits=dict(c=(1, 1)),
        )

        mg.set_data(data=self.data, x="x", y="y", crs=3857)
        mg.set_classify_specs(scheme=Maps.CLASSIFIERS.EqualInterval, k=4)

        for m in mg:
            m.plot_map()

        mg.add_annotation(ID=520)
        mg.add_marker(ID=5, fc="r", radius=10, radius_crs=4326)

        self.assertTrue(mg.m_a is mg["a"])
        self.assertTrue(mg.m_2 is mg[2])
        self.assertTrue(mg.ax_c is mg["c"])

        plt.close(mg.f)

        with self.assertRaises(AssertionError):
            MapsGrid(
                2,
                2,
                m_inits={"2": (0, slice(0, 2)), 2: (1, 0)},
                ax_inits=dict(c=(1, 1)),
            )

        with self.assertRaises(AssertionError):
            MapsGrid(
                2,
                2,
                m_inits={1: (0, slice(0, 2)), 2: (1, 0)},
                ax_inits={"2": (1, 1), 2: 2},
            )

    def test_compass(self):
        m = Maps(Maps.CRS.Stereographic())
        m.add_feature.preset.coastline(ec="k", scale="110m")
        c1 = m.add_compass((0.1, 0.1))
        self.assertTrue(np.allclose(c1.get_position(), np.array([0.1, 0.1])))
        c2 = m.add_compass((0.9, 0.9))
        self.assertTrue(np.allclose(c2.get_position(), np.array([0.9, 0.9])))

        cv = m.f.canvas

        # click on compass to move it around
        button_press_event(cv, *m.ax.transAxes.transform((0.1, 0.1)), 1, False)
        motion_notify_event(cv, *m.ax.transAxes.transform((0.5, 0.5)), False)
        button_release_event(cv, *m.ax.transAxes.transform((0.5, 0.5)), 1, False)

        c1.set_position((-30000000, -2000000))
        c1.set_patch("r", "g", 5)
        c1.set_pickable(False)
        c1.remove()

        c2.set_position((0.75, 0.25), "axis")
        c2.set_patch((1, 0, 1, 0.5), False)
        c2.remove()

        c = m.add_compass((0.5, 0.5), scale=7, style="north arrow", patch="g")
        c.set_position((-30000000, -2000000))
        c.set_patch("r", "g", 5)
        c.set_position((0.75, 0.25), "axis")
        c.set_patch((1, 0, 1, 0.5), False)
        c.set_pickable(False)

        plt.close("all")

    def test_ScaleBar(self):

        m = Maps()
        m.add_feature.preset.ocean(ec="k", scale="110m")

        s = m.add_scalebar(scale=250000)
        s.set_position(10, 20, 30)
        s.set_label_props(every=2, scale=1.25, offset=0.5, weight="bold")
        s.set_scale_props(n=6, colors=("k", "r"))
        s.set_patch_props(offsets=(1, 1.5, 1, 0.75))

        s1 = m.add_scalebar(
            -31,
            -50,
            90,
            scale=500000,
            scale_props=dict(n=10, width=3, colors=("k", ".25", ".5", ".75", ".95")),
            patch_props=dict(fc=(1, 1, 1, 1)),
            label_props=dict(every=5, weight="bold", family="Calibri"),
        )

        s2 = m.add_scalebar(
            -45,
            45,
            45,
            scale=500000,
            scale_props=dict(n=6, width=3, colors=("k", "r")),
            patch_props=dict(fc="none", ec="r", lw=0.25, offsets=(1, 1, 1, 1)),
            label_props=dict(rotation=45, weight="bold", family="Impact"),
        )

        s3 = m.add_scalebar(
            78,
            -60,
            0,
            scale=250000,
            scale_props=dict(n=20, width=3, colors=("k", "w")),
            patch_props=dict(fc="none", ec="none"),
            label_props=dict(scale=1.5, weight="bold", family="Courier New"),
        )

        # test_presets
        s_bw = m.add_scalebar(preset="bw")

        # ----------------- TEST interactivity
        cv = m.f.canvas
        x, y = m.ax.transData.transform(s3.get_position()[:2])
        x1, y1 = (
            (m.f.bbox.x0 + m.f.bbox.x1) / 2,
            (m.f.bbox.y0 + m.f.bbox.y1) / 2,
        )

        # click on scalebar
        button_press_event(cv, x, y, 1, False)

        # move the scalebar
        motion_notify_event(cv, x1, y1, False)

        # increase bbox size
        key_press_event(cv, "left")
        key_press_event(cv, "right")
        key_press_event(cv, "up")
        key_press_event(cv, "down")

        # deincrease bbox size
        key_press_event(cv, "alt+left")
        key_press_event(cv, "alt+right")
        key_press_event(cv, "alt+up")
        key_press_event(cv, "alt+down")

        # rotate the scalebar
        key_press_event(cv, "+")
        key_press_event(cv, "-")

        # adjust the padding between the ruler and the text
        key_press_event(cv, "alt+-")
        key_press_event(cv, "alt++")

        for si in [s, s1, s2, s3, s_bw]:
            si.remove()

        plt.close("all")

    def test_set_extent_to_location(self):
        m = Maps()
        resp = m._get_nominatim_response("austria")

        m.add_feature.preset.countries()
        m.set_extent_to_location("Austria")

        e = m.ax.get_extent()
        bbox = list(map(float, resp["boundingbox"]))

        self.assertTrue(np.allclose([e[2], e[3], e[0], e[1]], bbox, atol=0.1))

    def test_adding_maps_to_existing_figures(self):
        # use existing axes
        f = plt.figure()
        ax = f.add_subplot(projection=Maps.CRS.PlateCarree())
        m = Maps(ax=ax)
        m.add_feature.preset.coastline()

        # absolute positioning
        f = plt.figure()
        m1 = Maps(f=f, ax=(0.4, 0.4, 0.5, 0.5))
        m2 = Maps(f=f, ax=(0.05, 0.05, 0.4, 0.4))
        m1.add_feature.preset.coastline()
        m2.add_feature.preset.coastline()
        plt.close(f)

        # grid positioning
        f, ax = plt.subplots()
        m = Maps(f=f, ax=211)
        m.add_feature.preset.coastline()
        plt.close(f)

        f, ax = plt.subplots()
        m = Maps(f=f, ax=(2, 1, 1))
        m.add_feature.preset.coastline()
        plt.close(f)

        gs = GridSpec(2, 2)
        f, ax = plt.subplots()
        m = Maps(f=f, ax=gs[1, 1])
        m.add_feature.preset.coastline()
        plt.close(f)

        f = plt.figure()
        ax = f.add_subplot(221)
        ax2 = f.add_subplot(222)
        m1 = Maps(f=f, ax=223)
        m2 = Maps(f=f, ax=224)

        m1.add_feature.preset.coastline()
        m2.add_feature.preset.coastline()

    def test_a_complex_figure(self):
        # %%
        lon, lat = np.linspace(-180, 180, 500), np.linspace(-90, 90, 500)
        lon, lat = np.meshgrid(lon, lat)

        df = pd.DataFrame(
            dict(lon=lon.flat, lat=lat.flat, data=(lon**2 + lat**2).flat)
        )

        crs = [
            Maps.CRS.Stereographic(),
            Maps.CRS.Sinusoidal(),
            Maps.CRS.Mercator(),
            #
            Maps.CRS.EckertI(),
            Maps.CRS.EckertII(),
            Maps.CRS.EckertIII(),
            #
            Maps.CRS.EckertIV(),
            Maps.CRS.EckertV(),
            Maps.CRS.Mollweide(),
            #
            Maps.CRS.Orthographic(central_longitude=45, central_latitude=45),
            Maps.CRS.AlbersEqualArea(),
            Maps.CRS.LambertCylindrical(),
        ]

        mgrid = MapsGrid(3, 4, crs=crs, figsize=(12, 10))
        mgrid.set_data(
            data=df.sample(2000),
            x="lon",
            y="lat",
            crs=4326,
            encoding=dict(scale_factor=1e-6),
        )

        for i, m, title in zip(
            (
                ["ellipses", dict(radius=1.0, radius_crs="in")],
                ["ellipses", dict(radius=100000, radius_crs="out")],
                ["geod_circles", dict(radius=100000)],
                #
                ["rectangles", dict(radius=1.5, radius_crs="in")],
                ["rectangles", dict(radius=100000, radius_crs="out")],
                ["rectangles", dict(radius=1.5, radius_crs="in", mesh=True)],
                #
                ["rectangles", dict(radius=100000, radius_crs="out", mesh=True)],
                ["voronoi_diagram", dict(mask_radius=200000)],
                ["voronoi_diagram", dict(masked=False)],
                #
                [
                    "delaunay_triangulation",
                    dict(mask_radius=(100000, 100000), mask_radius_crs="in"),
                ],
                [
                    "delaunay_triangulation",
                    dict(mask_radius=100000, mask_radius_crs="out"),
                ],
                ["delaunay_triangulation", dict(masked=False)],
            ),
            list(mgrid),
            (
                "in_ellipses",
                "out_ellipses",
                "geod_circles",
                "in_rectangles",
                "out_rectangles",
                "in_trimesh_rectangles",
                "out_trimesh_rectangles",
                "voronoi",
                "voronoi_unmasked",
                "delaunay_flat",
                "delaunay",
                "delaunay_unmasked",
            ),
        ):

            print(title)

            m.ax.set_title(title)
            getattr(m.set_shape, i[0])(**i[1])

            m.plot_map(edgecolor="none")
            m.cb.click.attach.annotate(fontsize=6)
            m.add_feature.preset.coastline(lw=0.5)
            m.add_colorbar()

        mgrid.share_click_events()

        m.subplots_adjust(left=0.05, top=0.95, bottom=0.05, right=0.95)
        # %%
        plt.close(m.f)

    def test_alternative_inputs(self):
        lon, lat = np.mgrid[20:40, 20:50]
        vals = lon + lat

        # 2D numpy array
        m = Maps()
        m.set_data(vals, x=lon, y=lat)
        m.plot_map()

        # 1D numpy array
        m = Maps()
        m.set_data(vals.ravel(), x=lon.ravel(), y=lat.ravel())
        m.plot_map()

        # 1D lists
        m = Maps()
        m.set_data(
            vals.ravel().tolist(),
            x=lon.ravel().tolist(),
            y=lat.ravel().tolist(),
        )
        m.plot_map()

    def test_add_feature(self):
        m = Maps()
        m.add_feature.preset.ocean()
        m.add_feature.preset.land()
        m.add_feature.preset.countries()
        m.add_feature.preset.coastline()

        plt.close("all")

        # test providing custom args
        m = Maps()
        countries = m.add_feature.cultural.admin_0_countries
        countries(ec="k", fc="g", scale=110)

        m.add_feature.physical.ocean(fc="b", scale=110)

        plt.close("all")

        # test MapsGrid functionality
        mg = MapsGrid()

        mg.add_feature.preset.ocean()
        mg.add_feature.preset.land()
        mg.add_feature.preset.countries()
        mg.add_feature.preset.coastline()

        plt.close("all")

    def test_decode_encode_data(self):
        encoded = np.array([1000, 2000, 3000])

        m = Maps()
        m.set_data(
            encoded,
            [1, 2, 3],
            [1, 2, 3],
            encoding=dict(scale_factor=0.01, add_offset=100),
        )
        m.plot_map()

        decoded = np.array(encoded) * 0.01 + 100

        self.assertTrue(np.allclose(m._decode_values(encoded), decoded))
        self.assertTrue(
            np.allclose(m._encode_values(m._decode_values(encoded)), encoded)
        )

    def test_maps_as_contextmanager(self):
        # just some very basic tests if cleanup functions do their job
        with Maps(layer="first") as m:
            m.set_data(*[[1, 2, 3]] * 3)
            m.plot_map()
            m.cb.click.attach.annotate()
            m.redraw()  # redraw here to force drawing (otherwise the data is NEVER shown!)
            self.assertTrue(
                all(
                    i in m._data_manager._all_data
                    for i in ["xorig", "yorig", "x0", "y0", "ids", "z_data"]
                )
            )
            self.assertTrue(
                all(
                    i in m._data_manager._current_data
                    for i in ["xorig", "yorig", "x0", "y0", "ids", "z_data"]
                )
            )

            self.assertTrue(len(m.cb.click.get.cbs) == 1)

            with m.new_layer("second") as m2:
                self.assertTrue(set(m._get_layers()) == {"first", "second"})

                m2.set_data(*[[1, 2, 3]] * 3)
                m2.plot_map()
                m2.cb.click.attach.annotate()
                m2.show()  # show the layer to trigger drawing
                self.assertTrue(
                    all(
                        i in m2._data_manager._all_data
                        for i in ["xorig", "yorig", "x0", "y0", "ids", "z_data"]
                    )
                )
                self.assertTrue(
                    all(
                        i in m2._data_manager._current_data
                        for i in ["xorig", "yorig", "x0", "y0", "ids", "z_data"]
                    )
                )

                self.assertFalse(m2.coll is None)
                self.assertTrue(len(m2.cb.click.get.cbs) == 1)

            self.assertTrue(set(m._get_layers()) == {"first"})

            self.assertTrue(len(m2._data_manager._all_data) == 0)
            self.assertTrue(len(m2._data_manager._current_data) == 0)

            self.assertTrue(
                all(
                    i in m._data_manager._all_data
                    for i in ["xorig", "yorig", "x0", "y0", "ids", "z_data"]
                )
            )
            self.assertTrue(
                all(
                    i in m._data_manager._current_data
                    for i in ["xorig", "yorig", "x0", "y0", "ids", "z_data"]
                )
            )
            self.assertTrue(len(m.cb.click.get.cbs) == 1)
            self.assertTrue(len(m.cb.click.get.cbs) == 1)

            self.assertTrue(m2.coll is None)
            self.assertTrue(len(m2.cb.click.get.cbs) == 0)

        self.assertTrue(m.coll is None)
        self.assertTrue(len(m.cb.click.get.cbs) == 0)

        self.assertTrue(len(m._data_manager._all_data) == 0)
        self.assertTrue(len(m._data_manager._current_data) == 0)

    def test_cleanup(self):
        m = Maps()
        m.add_annotation(xy=(45, 45))
        m.add_marker(xy=(45, 45))
        m.set_data(*[[1, 2, 3]] * 3)
        m.plot_map()
        m.cb.click.attach.annotate()
        m.cb.pick.attach.annotate()
        m.cb.keypress.attach.fetch_layers()
        m.redraw()  # redraw since otherwise the map might not yet be created!
        self.assertTrue(len(m.BM._artists[m.layer]) == 2)
        self.assertTrue(len(m.BM._bg_artists[m.layer]) == 1)

        self.assertTrue(m._data_manager.x0.size == 3)
        self.assertTrue(hasattr(m, "tree"))
        self.assertTrue(len(m.cb.click.get.cbs) == 1)
        self.assertTrue(len(m.cb.click.get.cbs) == 1)
        self.assertTrue(len(m.cb.click.get.cbs) == 1)

        # test cleaning a new layer
        m2 = m.new_layer("asdf")
        m2.add_annotation(xy=(45, 45))
        m2.add_marker(xy=(45, 45))
        m2.set_data(*[[1, 2, 3]] * 3)
        m2.plot_map()
        m2.cb.click.attach.annotate()
        m2.cb.pick.attach.annotate()
        m2.cb.keypress.attach.fetch_layers()

        m2.on_layer_activation(lambda m: print("temporary", m.layer))
        m2.on_layer_activation(lambda m: print("permanent", m.layer), persistent=True)

        self.assertTrue(len(m.BM._on_layer_activation[m2.layer]) == 2)
        m2.show()  # show the layer to draw the artists!
        m.redraw()  # redraw since otherwise the map might not yet be created!
        self.assertTrue(len(m.BM._on_layer_activation[m2.layer]) == 1)

        self.assertTrue(len(m.BM._artists[m.layer]) == 2)
        self.assertTrue(len(m.BM._bg_artists[m.layer]) == 1)
        self.assertTrue(len(m.BM._artists[m2.layer]) == 2)
        self.assertTrue(len(m.BM._bg_artists[m2.layer]) == 1)

        self.assertTrue(m2._data_manager.x0.size == 3)
        self.assertTrue(hasattr(m2, "tree"))
        self.assertTrue(len(m2.cb.click.get.cbs) == 1)
        self.assertTrue(len(m2.cb.click.get.cbs) == 1)
        self.assertTrue(len(m2.cb.click.get.cbs) == 1)

        m2.cleanup()

        self.assertTrue(m2.layer not in m.BM._on_layer_activation)

        self.assertTrue(len(m.BM._artists[m.layer]) == 2)
        self.assertTrue(len(m.BM._bg_artists[m.layer]) == 1)
        self.assertTrue(m2.layer not in m.BM._artists)
        self.assertTrue(m2.layer not in m.BM._bg_artists)

        # m should still be OK
        self.assertTrue(m._data_manager.x0.size == 3)
        self.assertTrue(hasattr(m, "tree"))
        self.assertTrue(len(m.cb.click.get.cbs) == 1)
        self.assertTrue(len(m.cb.click.get.cbs) == 1)
        self.assertTrue(len(m.cb.click.get.cbs) == 1)

        # m2 must already be cleared
        self.assertTrue(m2._data_manager.x0 is None)
        self.assertTrue(not hasattr(m2, "tree"))
        self.assertTrue(len(m2.cb.click.get.cbs) == 0)
        self.assertTrue(len(m2.cb.click.get.cbs) == 0)
        self.assertTrue(len(m2.cb.click.get.cbs) == 0)

        m.cleanup()

        self.assertTrue(m.layer not in m.BM._artists)
        self.assertTrue(m.layer not in m.BM._bg_artists)

        self.assertTrue(m._data_manager.x0 is None)
        self.assertTrue(not hasattr(m, "tree"))
        self.assertTrue(len(m.cb.click.get.cbs) == 0)
        self.assertTrue(len(m.cb.click.get.cbs) == 0)
        self.assertTrue(len(m.cb.click.get.cbs) == 0)

    def test_blit_artists(self):
        # just a sanity-check if function throws an error...
        m = Maps()
        line = plt.Line2D(
            [0, 0.25, 1], [0, 0.63, 1], c="k", lw=3, transform=m.ax.transAxes
        )
        m.BM.blit_artists([line])
