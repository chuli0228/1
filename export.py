from odoo import fields, models, api
import base64
import xlwt
from io import BytesIO
from datetime import datetime


class ExportWizard(models.Model):
    _name = 'library.export'
    _description = 'export'
    file = fields.Binary('文件')

    def generated_excel_report(self, library_ids):

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('SYS')
        style0 = xlwt.XFStyle()  # 初始化样式 标题栏
        style1 = xlwt.XFStyle()  # 初始化样式 写入内容
        #字体设置
        font = xlwt.Font()  # 创建字体
        font.name = u'Meiryo UI'  # 字体
        font.height = 240  # 字体大小 240相当于12
        font.bold = True  # 字体加粗
        font.colour_index = 0  # 字体颜色设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow
        font1 = xlwt.Font()  # 创建字体
        font1.name = u'Meiryo UI'  # 字体
        font1.height = 200  # 字体大小 200相当于10
        style0.font = font  # 设定样式
        style1.font = font1  # 初始化样式

        # 单元格边框设置
        borders = xlwt.Borders()  # Create Borders
        borders.left = xlwt.Borders.THIN  # DASHED虚线 NO_LINE没有 THIN实线
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.DASHED
        borders.left_colour = 0
        borders.right_colour = 0
        borders.top_colour = 0
        borders.bottom_colour = 0
        style0.borders = borders  # Add Borders to Style

        borders1 = xlwt.Borders()  # Create Borders
        borders1.left = xlwt.Borders.THIN  # DASHED虚线 NO_LINE没有 THIN实线
        borders1.right = xlwt.Borders.THIN
        borders1.top = xlwt.Borders.THIN
        borders1.bottom = xlwt.Borders.THIN
        borders1.DASHED
        borders1.left_colour = 0
        borders1.right_colour = 0
        borders1.top_colour = 0
        borders1.bottom_colour = 0
        style1.borders = borders1  # Add Borders to Style

        # 单元格宽度设置
        worksheet.col(0).width = 12 * 256    # 郵便先
        worksheet.col(1).width = 13 * 256    # 提出部門
        worksheet.col(2).width = 5 * 256     # No.
        worksheet.col(3).width = 10 * 256    # 送信元
        worksheet.col(4).width = 11 * 256    # 氏名
        worksheet.col(5).width = 17 * 256    # 郵便番号
        worksheet.col(6).width = 76 * 256    # 住所
        worksheet.col(7).width = 48 * 256    # 会社名
        worksheet.col(8).width = 42 * 256    # 所属１
        worksheet.col(9).width = 42 * 256    # 所属2
        worksheet.col(10).width = 15 * 256   # 役職
        worksheet.col(11).width = 7 * 256    # 課長
        worksheet.col(12).width = 34 * 256   # メール
        # 设置行高
        worksheet.row(0).height_mismatch = True
        worksheet.row(0).height = 360  # 设置行高 18

        # add header
        header = ['郵便先', '提出部門', 'No.', '送信元', '氏名', '郵便番号', '住所', '会社名', '所属１', '所属2', '役職',
                  '課長', 'メール']
        for col in range(len(header)):
            worksheet.write(0, col, header[col], style0)
        case = ['日本', 'DX-2', ' ', 'DX-2', '峯岸亨', '211-8520', '神奈川県川崎市中原区下小田中2-20-5',
                '富士通エフ・アイ・ピー株式会社(FIP)', 'サービスビジネス本部)ＥＤＩビジネス事業部', '第二公共システム部', '事業部長代理'
                , '丁宇胜', 'minegishi.toru@jp.fujitsu.com']
        # add data
        for row in range(1, len(library_ids)+1):
            worksheet.row(row).height_mismatch = True
            worksheet.row(row).height = 360  # 设置行高 18
            library_id = library_ids[row-1]
            author = ''
            num = 1
            for list0 in library_id.author_ids:
                if num != 1:
                    author = author + ', '+list0.name
                else:
                    author = list0.name
                num = num + 1

            worksheet.write(row, 0, str(library_id.name), style1)
            worksheet.write(row, 1, str(author), style1)
            worksheet.write(row, 2, str(library_id.publisher_id.name), style1)

        # for row in range(1, 20):
        #     worksheet.row(row).height_mismatch = True
        #     worksheet.row(row).height = 360  # 设置行高 18
        #     worksheet.write(row, 0, case[0], style1)
        #     worksheet.write(row, 1, case[1], style1)
        #     worksheet.write(row, 2, row, style1)
        #     worksheet.write(row, 3, case[3], style1)
        #     worksheet.write(row, 4, case[4], style1)
        #     worksheet.write(row, 5, case[5], style1)
        #     worksheet.write(row, 6, case[6], style1)
        #     worksheet.write(row, 7, case[7], style1)
        #     worksheet.write(row, 8, case[8], style1)
        #     worksheet.write(row, 9, case[9], style1)
        #     worksheet.write(row, 10, case[10], style1)
        #     worksheet.write(row, 11, case[11], style1)
        #     worksheet.write(row, 12, case[12], style1)

        # save
        buffer = BytesIO()
        workbook.save(buffer)
        return base64.encodebytes(buffer.getvalue())

    @api.multi
    def action_export(self):
        context = dict(self._context or {})  # 保证context的字典类型
        print('context=', context)
        active_ids = context.get('active_ids', []) or []
        print('active_ids=', active_ids)
        library_book_ids = self.env['library.book'].browse(active_ids)
        print('library_book_ids=', library_book_ids)
        res = self.create({'file': self.generated_excel_report(library_book_ids)})

        value = dict(
            type='ir.actions.act_url',
            target='new',
            url='/web/content?model=%s&id=%s&field=file&download=true&filename=library.xls' % (self._name, res.id),
        )
        return value





