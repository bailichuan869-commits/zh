import zipfile
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
ET.register_namespace("w", NS["w"])

NEW_TEXTS = [
    "本人自2022年11月起从事审计工作，2023年2月入职立信，至今已累计审计从业3年8个月。工作期间，先后参与长春捷翼汽车科技股份有限公司IPO项目、嘉事堂药业股份有限公司年审项目、山东凤祥股份有限公司年审项目、中航信托股份有限公司项目、内蒙古双欣环保材料股份有限公司IPO项目等大型项目，同时参与多项中小型鉴证及非鉴证业务。主要项目经历和工作业绩如下：",
    "一、长春捷翼汽车科技股份有限公司IPO项目",
    "项目背景：长春捷翼是一家先进的汽车线束制造企业。该项目由我所在团队承做，并于2023年6月申报沪市主板；后于2024年4月终止审核，2025年6月重启上市辅导。",
    "参与时间：2023年2月至2024年5月；2025年5月至今。",
    "主要工作业绩：1）作为项目组主要成员，负责成本、存货、应付账款及其他相关科目的核查工作；2）参与推动企业于2023年6月完成沪市主板申报，并配合项目组完成首轮问询反馈回复；3）全程深度参与公司ERP系统升级建设，结合审计核查需求对系统规则设置提出优化建议，并对系统输出结果的准确性、合理性进行复核，及时提出修改意见。",
    "二、嘉事堂药业股份有限公司年审项目",
    "项目背景：嘉事堂为深交所主板上市公司，是国内主要医药流通企业之一。2024年度审计为立信首次承接该公司年审业务。",
    "参与时间：2024年10月至2025年4月。",
    "主要工作业绩：1）作为项目组主要成员，负责收入、应收账款及其他相关科目的核查工作；2）面对首次承接、近100家子公司、内控审计与财务报表审计同步推进等情况，参与完成业务流程梳理、审计资料对接和重点科目核查，在较紧的时间安排下保障相关工作有序推进；3）配合项目组顺利出具上市公司年度审计报告。",
    "三、山东凤祥股份有限公司年审项目",
    "项目背景：山东凤祥是一家覆盖白羽鸡全产业链的食品企业，2020年在港股上市，并于2025年7月完成私有化。",
    "参与时间：2025年12月至2026年6月。",
    "主要工作业绩：1）作为项目组主要成员，负责成本、存货及其他相关科目的核查工作；2）围绕生产成本归集、存货收发存及期末结存等重点内容执行审计程序，配合项目组顺利出具年度审计报告。",
]


def non_empty_paragraphs(root):
    for paragraph in root.findall(".//w:p", NS):
        text_nodes = paragraph.findall(".//w:t", NS)
        text = "".join((node.text or "") for node in text_nodes).strip()
        if text:
            yield text_nodes


def main():
    parser = argparse.ArgumentParser(description="Polish a local audit work-performance DOCX.")
    parser.add_argument("source", type=Path, help="Source DOCX path.")
    parser.add_argument("output", type=Path, help="Output DOCX path.")
    args = parser.parse_args()
    with zipfile.ZipFile(args.source, "r") as zin:
        root = ET.fromstring(zin.read("word/document.xml"))
        paragraphs = list(non_empty_paragraphs(root))

        if len(paragraphs) != len(NEW_TEXTS):
            raise RuntimeError(
                f"Paragraph count mismatch: found {len(paragraphs)}, expected {len(NEW_TEXTS)}"
            )

        for nodes, text in zip(paragraphs, NEW_TEXTS):
            nodes[0].text = text
            for node in nodes[1:]:
                node.text = ""

        document_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = document_xml if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, data)

    print(args.output)


if __name__ == "__main__":
    main()
