from __future__ import annotations
from PySide6.QtWidgets import *

import math
import sys

from PySide6.QtCore import (QEasingCurve, QLineF,
                            QParallelAnimationGroup, QPointF,
                            QPropertyAnimation, QRectF, Qt)
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
import sys
import basicNode as BN


#https://doc.qt.io/qtforpython-6/examples/example_external_networkx.html 


class Window(QWidget):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setMinimumSize(300,200)
        self.setMaximumHeight(300)
        self.labelName = QLabel("Node Lable")
        self.editNodeName = QLineEdit()
        self.labelNode = QLabel("Node Value")
        self.editNode = QLineEdit()
        self.button = QPushButton("add")
        self.button.clicked.connect(self.addNode)
        self.container= QHBoxLayout(self)
        self.Gridlayout = QGridLayout()



        self.Gridlayout.addWidget(self.labelName,0,0)
        self.Gridlayout.addWidget(self.editNodeName,1,0)
        self.Gridlayout.addWidget(self.labelNode,0,1)
        self.Gridlayout.addWidget(self.editNode,1,1)
        self.Gridlayout.addWidget(self.button,2,0,1,2)
        


       
        
        self.Connect = QLabel("Connect node 2 to 1 ")
        self.node1 = QLabel("Node 1")
        self.editNode1Name = QLineEdit()
        self.node2 = QLabel("Node 2")
        self.editNode2Name = QLineEdit()
        self.connectBt = QPushButton("Connect")
        self.SeeNodes = QPushButton("see all nodes")
        

        self.SeeNodes.clicked.connect(self.seeAllNodes)
        self.connectBt.clicked.connect(self.connect)

        self.Gridlayout.addWidget(self.Connect, 3, 0, 1, 2)
        self.Gridlayout.addWidget(self.node1,4,0)
        self.Gridlayout.addWidget(self.node2,4,1)
        self.Gridlayout.addWidget(self.editNode1Name,5,0)
        self.Gridlayout.addWidget(self.editNode2Name,5,1)
        self.Gridlayout.addWidget(self.connectBt,6,0,1,2)
        self.Gridlayout.addWidget(self.SeeNodes,7,0,1,2)
        

        self.container.addLayout(self.Gridlayout)
        self.g = BN.Graph()

    def addNode(self):
        if hasattr(self, 'error') and self.error:
                self.error =QLabel("")
                self.Gridlayout.removeWidget(self.error)
        nodeLable = self.editNodeName.text().strip()
        nodeValue = self.editNode.text().strip()
        if nodeValue=="":
            if hasattr(self, 'error') and self.error:
                 self.error =QLabel("")
                 self.Gridlayout.removeWidget(self.error)
            self.error = QLabel("Need node value")
            self.Gridlayout.addWidget(self.error,8,0,1,2)
            return False
        if nodeLable=="":
            if hasattr(self, 'error') and self.error:
                self.error =QLabel("")
                self.Gridlayout.removeWidget(self.error)
            self.error = QLabel("Need node Lable")
            self.Gridlayout.addWidget(self.error,8,0,1,2)
            return False
       
        

        node = BN.Node(nodeLable)
        self.g.addNode(node)
        self.editNode.clear()
        self.editNodeName.clear()

        
        self.seeAllNodes()

    def connect(self):
        if hasattr(self, 'error') and self.error:
                self.error =QLabel("")
                self.Gridlayout.removeWidget(self.error)
        node1 = self.editNode1Name.text().strip()
        node2 = self.editNode2Name.text().strip()
        
        found_node1 = None
        found_node2 = None
        
        if node1 == "" or node2 == "":
            if hasattr(self, 'error') and self.error:
                self.error =QLabel("")
                self.Gridlayout.addWidget(self.error)
            self.error =QLabel("Need to enter node to connect")
            self.Gridlayout.addWidget(self.error,8,0,1,2)
            return False
        
        for node in self.g.nodes:
            if node.label == node1:
                found_node1 = node
        
            if node.label == node2:
                found_node2 = node
    
        if found_node1 is None or found_node2 is None:
            if hasattr(self, 'error') and self.error:
                self.Gridlayout.removeWidget(self.error)
            self.error = QLabel("Nodes not found")
            self.Gridlayout.addWidget(self.error,8,0,1,2)
            return False
        

        

        self.g.connectNode(found_node1,found_node2)
        self.seeAllNodes()
    def seeAllNodes(self):

        if hasattr(self, 'viewer') and self.viewer:
            self.container.removeWidget(self.viewer)
    
        self.viewer = GraphViewer(self.g)
        self.container.addWidget(self.viewer,2)
        window.resize(600,250)
            
            




class NodeItem(QGraphicsObject):

    def __init__(self, node):
        super().__init__()

        self.node = node
        self.edges = []
        self.radius = 30
        self.rect = QRectF(0, 0, self.radius * 2, self.radius * 2)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def boundingRect(self):
        return self.rect

    def paint(self, painter,options, widget = None):

        painter.setRenderHints(QPainter.Antialiasing)

        painter.setPen(QPen(QColor("#06560F"), 2))
        painter.setBrush(QBrush(QColor("#5AD469")))

        painter.drawEllipse(self.rect)

        painter.setPen(Qt.white)
        painter.drawText(self.rect, Qt.AlignCenter, self.node.label)

    def add_edge(self, edge):
        self.edges.append(edge)

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()

        return super().itemChange(change, value)


class EdgeItem(QGraphicsItem):

    def __init__(self, source, dest):

        super().__init__()

        self.source = source
        self.dest = dest

        self.source.add_edge(self)
        self.dest.add_edge(self)

        self.line = QLineF()
        self.arrow_size = 15

        self.adjust()

    def adjust(self):

        self.prepareGeometryChange()

        self.line = QLineF(
            self.source.pos() + self.source.boundingRect().center(),
            self.dest.pos() + self.dest.boundingRect().center()
        )

    def boundingRect(self):

        extra = self.arrow_size

        return QRectF(self.line.p1(), self.line.p2()).normalized().adjusted(
            -extra, -extra, extra, extra
        )

    def paint(self, painter, option, widget=None):

        painter.setRenderHints(QPainter.Antialiasing)

        painter.setPen(QPen(QColor("#2BB53C"), 2))
        painter.drawLine(self.line)

        self.draw_arrow(painter)

    def draw_arrow(self, painter):

        line = QLineF(self.line.p2(), self.line.p1())

        angle = math.atan2(-line.dy(), line.dx())

        arrow_p1 = line.p1() + QPointF(
            math.sin(angle + math.pi / 3) * self.arrow_size,
            math.cos(angle + math.pi / 3) * self.arrow_size
        )

        arrow_p2 = line.p1() + QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self.arrow_size,
            math.cos(angle + math.pi - math.pi / 3) * self.arrow_size
        )

        arrow_head = QPolygonF([line.p1(), arrow_p1, arrow_p2])

        painter.setBrush(QColor("#2BB53C"))
        painter.drawPolygon(arrow_head)


class GraphViewer(QGraphicsView):

    def __init__(self, graph):

        super().__init__()

        self.graph = graph
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.node_items = {}

        self.load_graph()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
     

    def load_graph(self):

        spacing = 150

        # create node items
        for i, node in enumerate(self.graph.nodes):

            item = NodeItem(node)

            x = (i % 5) * spacing
            y = (i // 5) * spacing

            item.setPos(x, y)

            self.scene.addItem(item)

            self.node_items[node] = item

        # create edges
        for vertex in self.graph.vertices:

            source = self.node_items[vertex.GetNode1()]
            dest = self.node_items[vertex.GetNode2()]

            edge = EdgeItem(source, dest)

            self.scene.addItem(edge)




app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()