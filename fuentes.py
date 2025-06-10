class Fuente:
    """Interfaz básica para fuentes de eventos."""

    def obtener_eventos(self):
        """Devuelve una lista de diccionarios con claves titulo, fecha y enlace."""
        raise NotImplementedError


import logging
import requests
from bs4 import BeautifulSoup


class EventbriteFuente(Fuente):
    """Eventos de Eventbrite en Madrid."""

    def obtener_eventos(self):
        url = 'https://www.eventbrite.es/d/spain--madrid/tecnologia/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("Error al obtener Eventbrite: %s", e)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        for card in soup.select('div.eds-event-card-content__content'):
            try:
                titulo = card.select_one('div.eds-event-card-content__title').text.strip()
                fecha = card.select_one('div.eds-event-card-content__sub-title').text.strip()
                enlace = card.find_parent('a')['href']
                eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
            except Exception:
                continue
        return eventos


class MeetupFuente(Fuente):
    """Eventos de Meetup filtrados por 'tech' en Madrid."""

    def obtener_eventos(self):
        url = 'https://www.meetup.com/find/events/?allMeetups=true&keywords=tech&radius=10&userFreeform=Madrid%2C+Spain'
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("Error al obtener Meetup: %s", e)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        for card in soup.select('li[data-eventid]'):
            try:
                titulo = card.select_one('h3 span').text.strip()
                fecha = card.select_one('time').text.strip()
                enlace = card.find('a', href=True)['href']
                if not enlace.startswith('http'):
                    enlace = 'https://www.meetup.com' + enlace
                eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
            except Exception:
                continue
        return eventos


class GDGFuente(Fuente):
    """Eventos de GDG Madrid."""

    def obtener_eventos(self):
        url = 'https://gdg.community.dev/gdg-madrid/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("Error al obtener GDG: %s", e)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        for card in soup.select('div.event-card'):
            try:
                titulo = card.select_one('h3').text.strip()
                fecha = card.select_one('time').text.strip()
                enlace = card.find('a', href=True)['href']
                eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
            except Exception:
                continue
        return eventos


class OpenExpoFuente(Fuente):
    """Eventos de OpenExpo."""

    def obtener_eventos(self):
        url = 'https://openexpoeurope.com/category/eventos/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("Error al obtener OpenExpo: %s", e)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        for card in soup.select('article'):
            try:
                titulo = card.select_one('h2.entry-title').text.strip()
                fecha = card.select_one('time').text.strip()
                enlace = card.find('a', href=True)['href']
                eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
            except Exception:
                continue
        return eventos


class CodemotionFuente(Fuente):
    """Eventos de Codemotion en Madrid."""

    def obtener_eventos(self):
        url = 'https://community.codemotion.com/events?city=Madrid'
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("Error al obtener Codemotion: %s", e)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        for card in soup.select('div.event-card'):
            try:
                titulo = card.select_one('h3').text.strip()
                fecha = card.select_one('.event-date').text.strip()
                enlace = card.find('a', href=True)['href']
                eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
            except Exception:
                continue
        return eventos


class HackathonFuente(Fuente):
    """Eventos de Hackathon.com en Madrid."""

    def obtener_eventos(self):
        url = 'https://www.hackathon.com/country/spain?city=Madrid'
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("Error al obtener Hackathon: %s", e)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        eventos = []
        for card in soup.select('div.hackathon-card'):
            try:
                titulo = card.select_one('h5').text.strip()
                fecha = card.select_one('.date').text.strip()
                enlace = card.find('a', href=True)['href']
                if not enlace.startswith('http'):
                    enlace = 'https://www.hackathon.com' + enlace
                eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
            except Exception:
                continue
        return eventos


# Lista util para combinarlas todas
todas = [
    EventbriteFuente(),
    MeetupFuente(),
    GDGFuente(),
    OpenExpoFuente(),
    CodemotionFuente(),
    HackathonFuente(),
]
