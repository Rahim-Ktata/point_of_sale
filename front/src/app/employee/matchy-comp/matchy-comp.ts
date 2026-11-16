import { AfterViewInit, Component, ElementRef, EventEmitter, inject, model, Output, ViewChild } from "@angular/core";
import { Matchy, UploadEntry } from "sheet-matchy";
import { EmployeeService } from "../../services/employee_service/employee-service";
import { MessageService } from "primeng/api";
import { matchy_options } from "../../utils";
import { Spinner } from '@primeicons/angular/spinner';
import { ToastModule } from 'primeng/toast';
import { DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';
import { MatchyUploadEntry } from "../../../models/interfaces/employee";


@Component({
  imports: [
    ToastModule,
    DialogModule, 
    ButtonModule,
  ],
  selector: 'app-matchy-comp',
  styleUrl: './matchy-comp.css',
  templateUrl: './matchy-comp.html',
})
export class MatchyComp implements AfterViewInit {
  matchy : Matchy | undefined;

  constructor(
    private employeeService: EmployeeService,
  ){}

  showImportEmpsDialog = model<boolean>(false);
  loading = model<boolean>(false);
  @Output() notify = new EventEmitter();
  private messageService = inject(MessageService);

  @ViewChild("matchy_container") container!: ElementRef<HTMLDivElement>;


  ngAfterViewInit() {
    this.matchy = new Matchy(matchy_options, {
      blockInvalidSubmit: true,
    });

    this.matchy.submit = async (data) => {
      this.importEmployees(data)
    };
    this.container.nativeElement.appendChild(this.matchy);
  }

  ximportEmployees(){
    this.showImportEmpsDialog.set(false);
    // let x = new UploadEntry()
  }

  importEmployees(entry:MatchyUploadEntry | any){
    this.messageService.add({
        severity: 'secondary',
        summary: 'Please wait...',
        detail: 'Your request is being processed. This may take a moment.',
        icon: 'pi pi-spinner pi-spin',
        key: 'promise',
        sticky: true
    });

    this.employeeService.bulkUploadEmployees(entry).subscribe({
      next : (data)=>{
          this.messageService.clear('promise');

          if(data.status_code == 200){
            this.messageService.add({ severity: 'success', summary: 'Uploaded successfully', detail: 'New employees have been added.' });

            // refresh table with new data
            this.loading.set(true);
            this.notify.emit();
          }

          else if(data.wrong_cells.length>0){

            // this.matchy?.markWrongCells(data.wrong_cells);
            const display = this.matchy?.shadow.getElementById("errorDisplay");
            display?.classList.remove("success");
            display!.textContent! = "some unique fields are duplicated or already exist in database, fix the red cells and submit again. Hover on the red cells for details.";
            this.messageService.add({ severity: 'error', summary: 'Invalid data', detail: "Uploaded file have errors" });

            this.matchy?.wrongCells.push(...data.wrong_cells)
            for(let x of data.wrong_cells){
              let key = `${x.rowIndex},${x.colIndex}`
              this.matchy?.cellIssues.set(key,x.issues);
            }
            this.matchy?.paintRenderedCells()
            // this.matchy?.updateErrorDisplay()
          }
          // errs => missing col
          else if(data.errs.length>0){
            this.messageService.add({ severity: 'error', summary: 'Missing mandatory columns', detail: "Uploaded file is missing mandatory fileds" });
          }
          else{
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: "Sth went wrong" });
          }

        },
      error : (error) => {

            console.log(this.matchy?.cellIssues!)
        this.messageService.clear('promise');

        if(error.error.detail){
          this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: error.detail });
        }
        else{
          this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: "We couldn’t complete the action." });
        }
      }
    })

    // this.showImportEmpsDialog.set(false);
  }
}


    // removeCellState(cell, state) {
    //     cell.classList.remove(state);
    //     cell.classList.remove(bootstrap[state]);
    // }
    // addCellState(cell, state) {
    //     cell.classList.add(state);
    //     cell.classList.add(bootstrap[state]);
    // }