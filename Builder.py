class Builder():
    def get_block(self, block_type='', **kwargs):
        if block_type == 'VIDEO':
            return f'<div><iframe title="YouTube video player" src="{kwargs["video_link"]}" width="100%" height="450" ' \
                   f'frameborder="0" allowfullscreen="allowfullscreen"></iframe>\n'
        elif block_type == 'START':
            return f'<div><div style="width: 80%; margin-left: auto; margin-right: auto;">\n' \
                   f'<h1 style="text-align: center;">{kwargs["title"]}</h1>\n<div><p>{kwargs["description"]}</p></div></div>\n'
        elif block_type == 'OVERVIEW':
            return f'<div class="f-grid-4"><img style="width: 50px;" src="{kwargs["image"]}" alt="" />' \
                   f'<p>{kwargs["description"]}</p></div>\n'
        elif block_type == 'IMAGE':
            return f'<div class="obrazek"><p><img src="{kwargs["image"]}" alt="" width="100%" /></p>' \
                   f'<div class="text-block">{kwargs["description"]}</div></div>\n'
        elif block_type == 'BLOCK':
            return f'<div class="f-grid-4"><img style="width: 200px;" src="{kwargs["image"]}" alt="" />' \
                   f'<h3>{kwargs["title"]}</h3>' \
                   f'<p>{kwargs["description"]}</p></div>\n'
        else:
            raise (TypeError, 'Wrong block type!')

    def build_description_from_dictionary(self, data):
        # Set up variables
        description = ''
        block_count = 0

        # Check if there's video and append it to description
        if data['VIDEO'] != '':
            description += self.get_block('VIDEO', video_link=data['VIDEO'])
        # Get description start
        description += self.get_block('START', title=data['START'][0], description=data['START'][1])
        # Begin setting up blocks
        description += '<div class="f-row">\n'
        # Get all overview blocks and break it in parts of 3
        for item in data['OVERVIEW']:
            if block_count % 3 == 0 and block_count != 0:
                description += '</div><div class="f-row">\n'
            description += self.get_block('OVERVIEW', image=item[0], description=item[1])
            block_count += 1
        description += '</div">\n'
        # Get description blocks. PC-LIFE-STYLE is wide image and PC-FEATURE-CARD is block with 3x1 patterns
        block_count = 0
        for item in data['DESCRIPTION']:
            if item[0] == 'pc-life-style':
                if block_count > 0:
                    description +='</div>\n'
                description += self.get_block('IMAGE', image=item[1], description=item[2])
            elif item[0] == 'pc-feature-card':
                if block_count % 3 == 0:
                    if block_count > 1 :
                        description += '</div>\n'
                    description += '<div class="f-row">\n'
                description += self.get_block('BLOCK',image=item[1],description=item[3],title='')
                block_count +=1
        description += '</div>\n'
        if len(data['DISCLAIMER']) > 0:
            description += '<div style="font-size: 8px;">\n'
            for item in data['DISCLAIMER']:
                description += f'<p><sup>{item[0]}</sup> {item[1]}</p>'
            description += '</div>\n'
        description += '</div>\n'
        return description
    def build_table(self,data):
        builded_table = '<table id="t01"><tbody>\n'
        for item in data:
            if item[0] == 'paragraph':
                builded_table += f'<tr class="title"><td colspan="2"><h2>{item[1]}</h2></td></tr>\n'
            elif item[0] == 'row':
                builded_table += f'<tr><th scope="row">{item[1]}</th>'
                if item[2] == 'yes':
                    builded_table += '<td class="yes"></td>'
                else:
                    builded_table += f'<td>{item[2]}</td>'
                builded_table += '</tr>\n'

        return builded_table
