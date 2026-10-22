import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

boutons = [['一', '丨', '丶', '丿', '乀', '乁', '乙', '乚', '乛', '亅'], ['二', '亠', '人', '儿', '入', '丷', '八', '冂', '冖', '冫', '几', '凵', '刀', '刂', '力', '勹', '匕', '匚', '匸', '十', '卜', '卩', '厂', '厶', '又', '讠'], ['口', '囗', '土', '士', '夂', '夕', '大', '女', '子', '宀', '寸', '小', '尢', '尸', '山', '巛', '川', '工', '己', '巾', '干', '幺', '广', '廴', '廾', '弋', '弓', '彐', '彑', '彡', '彳', '丬', '纟', '艹', '长', '门', '飞', '饣', '马'], ['心', '戈', '戶', '户', '手', '支', '攴', '攵', '文', '斗', '斤', '方', '无', '日', '曰', '月', '木', '欠', '止', '歹', '殳', '毋', '比', '毛', '氏', '气', '水', '火', '爪', '父', '爻', '爿', '片', '牙', '牛', '犬', '王', '肀', '月', '见', '贝', '车', '韦'], ['母', '玄', '玉', '瓜', '瓦', '甘', '生', '用', '甩', '田', '疋', '疒', '癶', '白', '皮', '皿', '目', '矛', '矢', '石', '示', '禸', '禾', '穴', '立', '罒', '龙'], ['竹', '米', '糸', '缶', '网', '羊', '羽', '老', '而', '耒', '耳', '聿', '肉', '臣', '自', '至', '臼', '舌', '舛', '舟', '艮', '色', '虍', '虫', '血', '行', '衣', '西', '辵', '页', '齐'], ['角', '言', '訁', '谷', '豆', '豕', '豸', '赤', '走', '足', '身', '車', '辛', '辰', '邑', '酉', '釆', '里', '鸟', '麦', '龟'], ['金', '阜', '隶', '隹', '雨', '青', '非', '鱼', '黾', '齿'], ['面', '革', '音', '风', '食', '首', '香'], ['骨', '高', '鬲', '鬼'], ['鹿', '麻', '黄'], ['黍', '黑'], ['鼎', '鼓', '鼠'], ['鼻']]

dico = {}

with open("raddict.txt") as f:
    for ligne in f:
        dico[ligne[0:1]] = set(ligne[2:])


class GridWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="RadDict")
        self.set_default_size(600, 900)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_child(main_box)

        self.set_child(scrolled)

        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(6)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_vexpand(True)
        main_box.append(grid)

        for ligne in range(len(boutons)):
            title = Gtk.Label(label=str(ligne + 1))
            title.set_xalign(0)
            title.add_css_class("row-title")
            main_box.append(title)

            flow = Gtk.FlowBox()
            flow.set_selection_mode(Gtk.SelectionMode.NONE)
            flow.set_homogeneous(True)
            flow.set_row_spacing(6)
            flow.set_column_spacing(6)
            flow.set_max_children_per_line(20)

            for chara in range(len(boutons[ligne])):
                button = Gtk.Button(label=str(boutons[ligne][chara]))
                #button.set_hexpand(True)
                button.set_vexpand(True)
                button.connect("clicked", self.on_button_clicked, str(boutons[ligne][chara]))
                flow.append(button)
            main_box.append(flow)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Radicaux...")
        self.entry.set_hexpand(True)
        main_box.append(self.entry)

        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        main_box.append(action_box)

        validate_button = Gtk.Button(label="Chercher")
        validate_button.set_hexpand(True)
        validate_button.connect("clicked", self.on_validate)
        action_box.append(validate_button)

        clear_button = Gtk.Button(label="Effacer")
        clear_button.set_hexpand(True)
        clear_button.connect("clicked", self.on_clear)
        action_box.append(clear_button)

        self.output_label = Gtk.Label(label="")
        self.output_label.set_selectable(True)
        self.output_label.set_wrap(True)
        self.output_label.set_xalign(0)
        self.output_label.add_css_class("output-label")
        self.output_label.set_margin_top(6)
        main_box.append(self.output_label)

        self.chari = Gtk.Entry()
        self.chari.set_placeholder_text("Charactère...")
        self.chari.set_hexpand(True)
        main_box.append(self.chari)

        decomp = Gtk.Button(label="Décomposer")
        decomp.set_hexpand(True)
        decomp.connect("clicked", self.decomposer)
        main_box.append(decomp)

        self.outd = Gtk.Label(label="")
        self.outd.set_selectable(True)
        self.outd.set_wrap(True)
        self.outd.set_xalign(0)
        self.outd.add_css_class("output-label")
        self.outd.set_margin_top(6)
        main_box.append(self.outd)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .output-label {
                padding: 8px;
                background-color: alpha(currentColor, 0.08);
                border-radius: 6px;
                font-family: monospace;
            }
            .row-title {
                font-weight: bold;
                font-size: 1.5em;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_button_clicked(self, _button, number):
        """Ajoute le numéro du bouton cliqué à la fin de l'entrée."""
        current = self.entry.get_text()
        self.entry.set_text(current + number)

    def on_validate(self, _button):
        """Copie le contenu de l'input vers le label d'output."""
        t = self.entry.get_text()
        charatrouve = []
        for (k, v) in dico.items():
            if set(t) < v:
                charatrouve += k
        self.output_label.set_text("".join(charatrouve))

    def on_clear(self, _button):
        """Vide l'input."""
        self.entry.set_text("")

    def decomposer(self, _button):
        try:
            decomp = dico[self.chari.get_text()]
            self.outd.set_text("".join(decomp))
        except KeyError:
            self.outd.set_text("Charactère non trouvé")


class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.raddict",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = GridWindow(self)
        win.present()


def main():
    app = App()
    app.run(None)


if __name__ == "__main__":
    main()
