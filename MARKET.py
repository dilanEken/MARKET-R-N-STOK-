# KULLANILACAK MODÜLLER
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3
from tkinter import *

# VERİ TABANI
veriler= sqlite3.connect('MARKET_ZİNCİRİ.db')
market = veriler.cursor()
market.execute("create table if not exists urun(urun_adi TEXT, urun_fiyati TEXT, urun_kdv TEXT)")
market.execute("create table if not exists stok(urun_id integer,urun_adi TEXT, adet integer)")
veriler.commit()

# UYARILAR
def kayıt_başarılı(text):
    mesaj = messagebox.showinfo(text, "Kayıt Başarılı...")
def kayıt_mevcut(text):
    mesaj = messagebox.showerror(text, "Bu isimde Ürün Mevcut...")
def kayıt_sil(text):
    mesaj = messagebox.showinfo(text, "Kayıt Silindi...")
def kayıt_güncele(text):
    mesaj = messagebox.showinfo(text, "Kaydınız Güncellendi...")

# MENÜ PENCERESİ
def Ana_Menü():
    for i in pen.winfo_children(): #eğer pen doluysa sil
        i.destroy()
    pen.title("ANA MENÜ")
    # ANA MENÜ TASLAĞI
    market_adi=Label(text="BÖTE MARKET",bg="#6200EA",fg="#BBDEFB",font="Helvetica""36")
    market_adi.place(x=120,y=10,width=300,height=70)
    urun_buton = Button(text="ÜRÜN EKRANI", command=Ürün_Pen,bg="#B71C1C",fg="#F3E5F5",font="Helvetica""36")
    urun_buton.place(x=30, y=200, width=200, height=80)
    stok_buton = Button(text="STOK EKRANI", command=stok_menu,bg="#B71C1C",fg="#F3E5F5",font="Helvetica""36")
    stok_buton.place(x=310, y=200, width=200, height=80)

# ÜRÜN MENÜSÜ PENCERESİ
def Ürün_Pen():
    # ÜRÜN KAYIT BÖLÜMÜ
    def Ürün_Ekle():
        ürün_ad = veri_adı.get()
        fiyat = veri_fiyatı.get()
        kdv = veri_kdv.get()

        def Ürünler():
            market.execute("insert into urun values(?,?,?)", [ürün_ad, fiyat, kdv])
            veriler.commit()
            #STOK VERI TABANINA YAZMA
            market.execute("""SELECT rowid,urun_adi FROM urun""")
            kontrol_ara = market.fetchall()
            for i in kontrol_ara:
                stok_ad_kontrol = i[1]
                ürün_id_no=i[0]
                if stok_ad_kontrol == ürün_ad:
                    market.execute("insert into stok values(?,?,?)", [ürün_id_no,ürün_ad, '0'])
                    veriler.commit()

        kod = 0
        market.execute("""SELECT urun_adi FROM urun""")
        kontrol = market.fetchall()
        for i in kontrol:  # KONTROL PANELİ ÜRÜNÜN OLUP OLMADIĞINI KONTROL EDER
            ad_kontrol = i[0]
            if ad_kontrol == ürün_ad:
                kayıt_mevcut("MALESEF AYNI KAYIT MEVCUT...")
                kod = 1
        if kod == 0:
            Ürünler()
            kayıt_başarılı("KAYIT YAPILDI...")
            veri_adı.delete(0, "end")
            veri_fiyatı.delete(0, "end")
            veri_kdv.delete(0, "end")
            for i in liste.get_children():
                liste.delete(i)
            market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
            urun_liste = market.fetchall()
            for i in urun_liste:
                liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))

    def Ürün_Silme():
        A = veri_adı.get()
        # STOKTAN KAYIT SILME
        market.execute("""SELECT rowid,urun_adi FROM urun""")
        kontrol_ara = market.fetchall()
        for i in kontrol_ara:
            stok_ad_kontrol = i[1]
            if stok_ad_kontrol == A:
                silmek=i[0]
        msg = messagebox.askyesno("SİLME İŞLEMİ", "EMİN MİSİN?")
        if msg == True:
            market.execute("delete from urun where urun_adi= ? ", [A])
            market.execute("delete from stok where urun_id= ? ", [silmek])
            veriler.commit()
            veri_adı.delete(0, "end")
            veri_fiyatı.delete(0, "end")
            veri_kdv.delete(0, "end")
            kayıt_sil("SİLME İŞLEMİ YAPILDI...")
            for i in liste.get_children():
                liste.delete(i)
            market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
            urun_liste = market.fetchall()
            for i in urun_liste:
                liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))

#KAYIT GÜNCELLEME
    def Ürün_Günceleme():
        veri_al = liste.selection()[0]
        item = liste.item(veri_al)
        sec_id_no = item['values'][0]
        # update kodu ile mevcut olan veriyi değiştirile bilir.
        market.execute("update urun set urun_adi='{}',urun_fiyati='{}',urun_kdv='{}' WHERE rowid='{}'".
                   format(veri_adı.get(),veri_fiyatı.get(),veri_kdv.get(),sec_id_no))
        veriler.commit()

        veri_adı.delete(0, "end")
        veri_fiyatı.delete(0, "end")
        veri_kdv.delete(0, "end")
        kayıt_güncele("KAYDINIZ GÜNCELENDİ...")
        for i in liste.get_children():
            liste.delete(i)
        market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
        urun_liste = market.fetchall()
        for i in urun_liste:
            liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))



    for i in pen.winfo_children():
        i.destroy() #Mevcut pencere temizleniyor
    pen.title("ÜRÜN") #ÜRÜN SAYFASI TASLAĞI OLUŞTURULUYOR
    Label(text="Ürün Adı", font="Helvetica 12 ").place(x=250, y=20)
    Label(text="Ürün Fiyatı", font="Helvetica 12 ").place(x=250, y=60)
    Label(text="KDV", font="Helvetica 12 ").place(x=250, y=95)
    veri_adı = Entry(width=35)
    veri_adı.place(x=330, y=20,height=28)
    veri_fiyatı = Entry(width=35)
    veri_fiyatı.place(x=330, y=60,height=28)
    veri_kdv = Entry(width=35)
    veri_kdv.place(x=330, y=95,height=28)
    #butonlar
    ürün_menü = Button(text="ANA MENÜ", command=Ana_Menü, font="Helvetica 12 ",bg="#1E88E5")
    ürün_menü.place(x=10, y=20, width=100, height=40)
    ürün_kaydet = Button(text="KAYDET", command=Ürün_Ekle,font="Helvetica 12 ",bg="#1E88E5")
    ürün_kaydet.place(x=130, y=20, width=100, height=40)
    ürün_yenile= Button(text="GÜNCELLE", command=Ürün_Günceleme,font="Helvetica 12 ",bg="#1E88E5")
    ürün_yenile.place(x=10, y=80, width=100, height=40)
    Silme_işlemi = Button(text="SİL", command=Ürün_Silme,font="Helvetica 12 ",bg="#1E88E5")
    Silme_işlemi.place(x=130, y=80, width=100, height=40)

    #SQLİTE verileri listeleme ve ekrana yansıtma
    liste = Treeview(pen)
    liste["columns"] = ("id_no", "Ad", "fiyat", "kdv")
    liste.column('#0', width=0, stretch=NO)
    liste.column('id_no', width=35, anchor=CENTER)
    liste.column('Ad', anchor=CENTER, width=180)
    liste.column('fiyat', anchor=CENTER, width=110)
    liste.column('kdv', anchor=CENTER, width=110)
    liste.place(x=15, y=140, width=520, height=250)
    liste.heading("#0", text="")
    liste.heading("id_no", text="ID")
    liste.heading("Ad", text="Ürün Adı")
    liste.heading("fiyat", text="Ürün Fiyatı")
    liste.heading("kdv", text="KDV %")
    # ürün veri tabanındaki veriler
    market.execute("""SELECT rowid,urun_adi,urun_fiyati, urun_kdv  FROM urun""")
    urun_liste = market.fetchall()
    for i in urun_liste:
        liste.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3]))

    def aktarma(object): # eğer veri giriş ekranında veri varsa temizle ve tabloda seçili veriyi giriş ekranına yansıt
        veri_adı.delete(0, "end")
        veri_fiyatı.delete(0, "end")
        veri_kdv.delete(0, "end")
        veri_al = liste.selection()[0]
        item = liste.item(veri_al)
        veri_adı.insert(0, item['values'][1])
        veri_fiyatı.insert(0, item['values'][2])
        veri_kdv.insert(0, item['values'][3])

    liste.bind("<Double-1>", aktarma)


# STOK MENÜSÜ PENCERESİ
def stok_menu():
    def stok_ekle_cikart(args):
        ekle = int(adet.get())
        ekli_ürün = combo.get()
        market.execute("""SELECT urun_adi,adet FROM stok""")
        kontrol_ara = market.fetchall()
        for i in kontrol_ara:
            stok_ad_kontrol = i[0]
            if stok_ad_kontrol == ekli_ürün:
                mevcut_stok = i[1]
        if args == 1:
            son_stok = mevcut_stok + ekle
        if args==2:
            son_stok = mevcut_stok - ekle
        market.execute("update stok set adet='{}' WHERE urun_adi='{}'".format(son_stok, ekli_ürün))
        veriler.commit()
        adet.delete(0, "end")
        for i in liste.get_children():
            liste.delete(i)
        market.execute("""SELECT urun_id,urun_adi, adet FROM stok""")
        stok_liste = market.fetchall()
        for i in stok_liste:
            liste.insert(parent='', index='end', values=(i[0], i[1], i[2]))

    for i in pen.winfo_children():
        i.destroy() #kayıtlı olan pencereyi temizler
    pen.title("STOK") #Yeni stok penceresi oluşturuluyor
    Stok_kaydet = Button(text="ÜRÜN EKLE",command=lambda:stok_ekle_cikart(1),bg="#1E88E5")
    Stok_kaydet.place(x=20, y=20, width=180, height=30)
    Stok_cık = Button(text="ÜRÜN ÇIKART",command=lambda:stok_ekle_cikart(2),bg="#1E88E5")
    Stok_cık.place(x=20, y=60, width=180, height=30)
    ana = Button(text="ANA MENÜ", command=Ana_Menü,bg="#1E88E5")
    ana.place(x=20, y=100, width=180, height=30)

    Label(text="Ürün Adı", font="Helvetica 12 ").place(x=266, y=40)
    Label(text="Ürün Adedi", font="Helvetica 12 ").place(x=266, y=80)

    combo= Combobox(width=28) #ÜRÜN TABLOSUNDAKİ VERİLERİ ALIP LİSTELİ ŞEKİLDE GÖSTERMESİ
    combo.place(x=350,y=40,height=30)
    market.execute("""SELECT urun_adi, adet FROM stok""")
    stok_liste = market.fetchall()
    for i in stok_liste:
        combo['values'] = tuple(list(combo['values']) + [str(i[0])])
    adet = Entry(width=31)
    adet.place(x=350, y=80,height=30)

    liste = Treeview(pen)
    liste["columns"] = ("id_no", "Ad", "adet")
    liste.column('#0', width=0, stretch=NO)
    liste.column('id_no', width=20, anchor=CENTER)
    liste.column('Ad', anchor=CENTER, width=220)
    liste.column('adet', anchor=CENTER, width=100)

    liste.place(x=20, y=140, width=460, height=180)
    liste.heading("#0", text="")
    liste.heading("id_no", text="ID")
    liste.heading("Ad", text="Ürün Adı")
    liste.heading("adet", text="Adet")

    market.execute("""SELECT urun_id,urun_adi, adet FROM stok""")
    stok_liste = market.fetchall()
    for i in stok_liste:
        liste.insert(parent='', index='end', values=(i[0],i[1],i[2]))

# PENCERE OLUŞTURMA
pen = tk.Tk()
pen.geometry("550x400+500+200")
pen.resizable(False, False)
Ana_Menü()

pen.mainloop()
