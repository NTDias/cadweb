from decimal import Decimal
import locale
import random
from django.db import models


#### CATEGORIA #####

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()


    def __str__(self):
        return self.nome

#### CLIENTE #######

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15,verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")


    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

### PRODUTO ####

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        # Tenta buscar o estoque, se não existir, cria um novo com qtde 0
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        print(flag_created)
        return estoque_item

    
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()


    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'



############ PEDIDO ####################

class Pedido(models.Model):


    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4


    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    ALIQUOTA_ICMS = 18.0
    ALIQUOTA_ICMS_ST = 5.0  # Exemplo, pode variar conforme o produto e estado
    ALIQUOTA_IPI = 4.0  # Se aplicável ao produto
    ALIQUOTA_PIS = 1.65
    ALIQUOTA_COFINS = 7.6

    @property
    def valor_icms(self):
        # Convertendo a alíquota para Decimal antes de multiplicar
        return (self.total * Decimal(str(self.ALIQUOTA_ICMS))) / 100

    @property
    def valor_ipi(self):
        return (self.total * Decimal(str(self.ALIQUOTA_IPI))) / 100

    @property
    def valor_pis(self):
        return (self.total * Decimal(str(self.ALIQUOTA_PIS))) / 100

    @property
    def valor_cofins(self):
        return (self.total * Decimal(str(self.ALIQUOTA_COFINS))) / 100

    @property
    def total_impostos(self):
        return self.valor_icms + self.valor_ipi + self.valor_pis + self.valor_cofins

    @property
    def total_com_impostos(self):
        return self.total + self.total_impostos
    @property
    def chave_acesso(self):
        """Gera uma chave fictícia de 44 dígitos."""
        random_part = "".join([str(random.randint(0, 9)) for _ in range(35)])
        return f"312410{random_part}{self.id:03d}".zfill(44)

    def __str__(self):
            return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None 
   
    @property
    def total(self):
        """Calcula o total de todos os itens no pedido."""
        # Soma (quantidade * preço) de todos os itens relacionados a este pedido
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total

    @property
    def qtdeItens(self):
        """Conta a quantidade de itens (linhas) no pedido."""
        return self.itempedido_set.count()
    
    @property
    def pagamentos(self):
        return self.pagamento_set.all()

    @property
    def total_pago(self):
        return sum(p.valor for p in self.pagamentos)

    @property
    def debito(self):
        return self.total - self.total_pago
    

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"  
    
    @property
    def total(self):
        """Calcula o total do item (quantidade * preço)."""
        return self.qtde * self.preco


############### PAGAMENTO ###############

class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4


    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None
       # lista de todos os pagamentos realiados
    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)    
    
    #Calcula o total de todos os pagamentos do pedido
 

