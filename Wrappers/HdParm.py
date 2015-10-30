import subprocess
import re

__author__ = 'm'

RootPassword = b'k'
InfoRegex = {
    'SerialNumber': re.compile("Serial Number:[ \t]*([^\n\t ]*)"),
    'ModelNumber': re.compile("Model Number:[ \t]*([0-9a-zA-Z_\(\)\-+., ]+)"),
    'FirmwareRevision': re.compile("Firmware Revision:[ \t]*([0-9a-zA-Z_\(\)\-+ ]+)")
}


class HdParm:
    InfoStr = ''
    SerialNumber = ''
    Path = ''
    ModelNumber = ''
    FirmwareRevision = ''

    @staticmethod
    def getinfofield(regexp, infostr):
        """
        Search hdparm -I output using a given regexp. If found, return the first
        matched group, otherwise None.
        :param regexp the regular expression to be used. Must contain a match group
        :param infostr output of "hdparm -I /dev/sdX" command
        :return: matched string or None
        """
        result = regexp.search(infostr)
        if result:
            return result.group(1)
        return None

    def __init__(self, path):
        self.Path = path
        self.getinfo()
        self.parseinfo()

    def getinfo(self):
        hdparm_shell = subprocess.Popen(
            ['sudo', '-S', 'hdparm', '-I', self.Path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        self.InfoStr = str(hdparm_shell.communicate(input=RootPassword + b"\n")[0])

    def parseinfo(self):
        self.SerialNumber = HdParm.getinfofield(InfoRegex['SerialNumber'], self.InfoStr)
        self.ModelNumber = HdParm.getinfofield(InfoRegex['ModelNumber'], self.InfoStr)
        self.FirmwareRevision = HdParm.getinfofield(InfoRegex['FirmwareRevision'], self.InfoStr)



"""
/dev/sdb:

ATA device, with non-removable media
	Model Number:       SAMSUNG SP1603C
	Serial Number:      S0CSJ1KP200399
	Firmware Revision:  VL100-50
Standards:
	Used: ATA/ATAPI-7 T13 1532D revision 4a
	Supported: 7 6 5 4 & some of 8
Configuration:
	Logical		max	current
	cylinders	16383	16383
	heads		16	16
	sectors/track	63	63
	--
	CHS current addressable sectors:   16514064
	LBA    user addressable sectors:  268435455
	LBA48  user addressable sectors:  312581808
	Logical/Physical Sector size:           512 bytes
	device size with M = 1024*1024:      152627 MBytes
	device size with M = 1000*1000:      160041 MBytes (160 GB)
	cache/buffer size  = 8192 KBytes (type=DualPortCache)
Capabilities:
	LBA, IORDY(can be disabled)
	Queue depth: 32
	Standby timer values: spec'd by Standard, no device specific minimum
	R/W multiple sector transfer: Max = 16	Current = 16
	Recommended acoustic management value: 254, current value: 0
	DMA: mdma0 mdma1 mdma2 udma0 udma1 udma2 udma3 udma4 udma5 *udma6 udma7
	     Cycle time: min=120ns recommended=120ns
	PIO: pio0 pio1 pio2 pio3 pio4
	     Cycle time: no flow control=120ns  IORDY flow control=120ns
Commands/features:
	Enabled	Supported:
	    	SMART feature set
	    	Security Mode feature set
	   *	Power Management feature set
	   *	Write cache
	   *	Look-ahead
	   *	Host Protected Area feature set
	   *	WRITE_BUFFER command
	   *	READ_BUFFER command
	   *	NOP cmd
	   *	DOWNLOAD_MICROCODE
	    	SET_MAX security extension
	    	Automatic Acoustic Management feature set
	   *	48-bit Address feature set
	   *	Device Configuration Overlay feature set
	   *	Mandatory FLUSH_CACHE
	   *	FLUSH_CACHE_EXT
	   *	SMART error logging
	   *	SMART self-test
	   *	General Purpose Logging feature set
	   *	Segmented DOWNLOAD_MICROCODE
	   *	Gen1 signaling speed (1.5Gb/s)
	   *	Gen2 signaling speed (3.0Gb/s)
	   *	Native Command Queueing (NCQ)
	   *	Host-initiated interface power management
	   *	Phy event counters
	   *	DMA Setup Auto-Activate optimization
	    	Device-initiated interface power management
	   *	Software settings preservation
	   *	SMART Command Transport (SCT) feature set
	   *	SCT Read/Write Long (AC1), obsolete
	   *	SCT Write Same (AC2)
	   *	SCT Error Recovery Control (AC3)
	   *	SCT Features Control (AC4)
	   *	SCT Data Tables (AC5)
Security:
	Master password revision code = 65534
		supported
	not	enabled
	not	locked
	not	frozen
	not	expired: security count
		supported: enhanced erase
	66min for SECURITY ERASE UNIT. 66min for ENHANCED SECURITY ERASE UNIT.
Checksum: correct
"""
